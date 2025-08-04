from app.repositories.request_repository import RequestLogRepository
from datetime import datetime
from app.entities.computation import Computation


class MathService:
    def __init__(self):
        self.repo = RequestLogRepository()

    async def compute(self, op: str, *args: int) -> int:
        if op == "pow":
            b, e = args
            return self._pow(b, e)
        elif op == "fib":
            n, = args
            return self._fib(n)
        elif op == "fact":
            n, = args
            return self._fact(n)
        else:
            raise ValueError(f"Unknown operation: {op}")

    async def submit_job(self, op: str, value: int) -> Computation:
        inp = str(value)

        comp = Computation(
            id=None,
            operation=op,
            input_value=inp,
            result=None,
            status="pending",
            timestamp=datetime.utcnow()
        )

        if await self.repo.exists(op, inp):
            raise ValueError(f"Calculation for {op!r} with input {inp!r} already exists")

        return await self.repo.create(comp)

    async def submit_pow_job(self, base: int, exponent: int) -> Computation:
        inp = f"{base}^{exponent}"
        comp = Computation(
            id=None,
            operation="pow",
            input_value=inp,
            result=None,
            status="pending",
            timestamp=datetime.utcnow()
        )
        if await self.repo.exists("pow", inp):
            raise ValueError(f"Calculation for pow with input {inp!r} already exists")
        return await self.repo.create(comp)

    async def update_result(self, comp: Computation, result: str) -> Computation:
        comp.set_result(result)
        comp.set_status("done")
        comp.set_timestamp(datetime.utcnow())
        return await self.repo.update(comp)

    async def get_job(self, job_id: int) -> Computation:
        comp = await self.repo.get_by_id(job_id)
        if not comp:
            raise ValueError(f"Job {job_id} not found")
        return comp

    async def get_by_operation_input(self, operation: str, input_value: str) -> Computation:
        comp = await self.repo.get_by_op_and_input(operation, input_value)
        if not comp:
            raise ValueError(f"No record for op={operation!r}, input={input_value!r}")
        return comp

    @staticmethod
    def _pow(base: int, exponent: int) -> int:
        return base ** exponent

    @staticmethod
    def _fib(n: int) -> int:
        a, b = 0, 1
        for _ in range(n):
            a, b = b, a + b
        return a

    @staticmethod
    def _fact(n: int) -> int:
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result
