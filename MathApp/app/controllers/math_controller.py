from fastapi import APIRouter, Depends, HTTPException, status, Body
from app.services.math_service import MathService
from app.workers.worker import queue
from app.utils.auth import verify_token
from app.utils.logger_queue import send_log
from app.schemas.compute_schema import ComputeRequest, PowRequest, JobResponse, ResultResponse

router = APIRouter(prefix="/api")


@router.post(
    "/compute",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=JobResponse
)
async def compute_operation(
    payload: ComputeRequest = Body(...),
    _: str = Depends(verify_token),
    service: MathService = Depends(MathService),
):
    operation = payload.operation
    value = payload.value

    if operation not in ("fib", "fact"):
        raise HTTPException(400, detail="Invalid operation for this endpoint")

    if value < 0:
        raise HTTPException(400, detail="Negative numbers are not allowed for this operation")

    try:
        comp = await service.submit_job(operation, value)
        job_id = comp.get_id()
        await send_log(f"Job accepted: id={job_id}, operation={operation}, value={value}")
    except ValueError as e:
        await send_log(f"Job rejected: operation={operation}, value={value}, reason={str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

    queue.put_nowait((job_id, operation, value))
    return {"job_id": job_id, "status": "pending"}


@router.post(
    "/compute/pow",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=JobResponse
)
async def compute_pow(
    payload: PowRequest = Body(...),
    _: str = Depends(verify_token),
    service: MathService = Depends(MathService),
):
    base = payload.base
    exponent = payload.exponent

    try:
        comp = await service.submit_pow_job(base, exponent)
        job_id = comp.get_id()
        await send_log(f"Job accepted: id={job_id}, operation=pow, input={base}^{exponent}")
    except ValueError as e:
        await send_log(f"Job rejected: operation=pow, input={base}^{exponent}, reason={str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

    queue.put_nowait((job_id, "pow", base, exponent))
    return {"job_id": job_id, "status": "pending"}


@router.get(
    "/results/{operation}/{input_value}",
    status_code=status.HTTP_200_OK,
    response_model=ResultResponse
)
async def get_result_by_input(
    operation: str,
    input_value: str,
    _: str = Depends(verify_token),
    service: MathService = Depends(MathService),
):
    try:
        job = await service.get_by_operation_input(operation, input_value)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return ResultResponse(
        operation=job.get_operation(),
        input=job.get_input_value(),
        result=job.get_result()
    )
