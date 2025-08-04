import asyncio
from sqlalchemy.exc import SQLAlchemyError
from app.services.math_service import MathService
from app.utils.logger_queue import send_log

queue: asyncio.Queue = asyncio.Queue()


async def start_worker():
    svc = MathService()
    while True:
        item = await queue.get()
        try:
            if item[1] == "pow":
                request_id, op, base, exponent = item
                res = await svc.compute(op, base, exponent)
            else:
                request_id, op, value = item
                res = await svc.compute(op, value)

            comp = await svc.get_job(request_id)
            await svc.update_result(comp, str(res))

            await send_log(f"Computation done: id={request_id}, result={res}")

        except ValueError as e:
            if op == "pow":
                _, _, base, exponent = item
                msg = f"Invalid request: pow({base}, {exponent}) - {e}"
            else:
                _, _, value = item
                msg = f"Invalid request: {op}({value}) - {e}"

            await send_log(msg)

        except SQLAlchemyError as e:
            msg = f"DB error for job {request_id}: {e}"
            await send_log(msg)

        except Exception as e:
            msg = f"Unexpected error for job {request_id}: {str(e)}"
            await send_log(msg)

        finally:
            queue.task_done()
