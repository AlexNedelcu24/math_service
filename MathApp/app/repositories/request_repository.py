from app.database.request_log import request_logs
from app.database.db import database
from app.entities.computation import Computation


class RequestLogRepository:

    @staticmethod
    async def create(computation: Computation) -> Computation:
        """
        Insert a new Computation into the DB,
         then set its id from the DB-generated value.
        """
        query = (
            request_logs.insert()
            .values(
                operation=computation.get_operation(),
                input_value=computation.get_input_value(),
                result=computation.get_result(),
                status=computation.get_status(),
                timestamp=computation.get_timestamp()
            )
        )
        new_id = await database.execute(query)
        computation.set_id(new_id)
        return computation

    @staticmethod
    async def update(computation: Computation) -> Computation:
        """
        Update an existing Computation in the DB by id, then return it.
        """
        query = (
            request_logs.update()
            .where(request_logs.c.id == computation.get_id())
            .values(
                result=computation.get_result(),
                status=computation.get_status(),
                timestamp=computation.get_timestamp()
            )
        )
        await database.execute(query)
        return computation

    @staticmethod
    async def get_by_id(request_id: int) -> Computation | None:
        """
        Fetch a Computation row by id and map it to a Computation object.
        """
        row = await database.fetch_one(
            request_logs.select().where(request_logs.c.id == request_id)
        )
        if not row:
            return None

        return Computation(
            id=row["id"],
            operation=row["operation"],
            input_value=row["input_value"],
            result=row["result"],
            status=row["status"],
            timestamp=row["timestamp"]
        )

    @staticmethod
    async def get_by_op_and_input(operation: str, input_value: str) -> Computation | None:
        """
        Fetch the most recent Computation for a given operation+input, map to Computation.
        """
        from sqlalchemy import desc

        row = await database.fetch_one(
            request_logs
            .select()
            .where(
                request_logs.c.operation == operation,
                request_logs.c.input_value == input_value
            )
            .order_by(desc(request_logs.c.timestamp))
            .limit(1)
        )
        if not row:
            return None

        return Computation(
            id=row["id"],
            operation=row["operation"],
            input_value=row["input_value"],
            result=row["result"],
            status=row["status"],
            timestamp=row["timestamp"]
        )

    @staticmethod
    async def exists(operation: str, input_value: str) -> bool:
        """
        Returns True if there is at least one record for operation+input_value.
        """
        row = await database.fetch_one(
            request_logs
            .select()
            .where(
                request_logs.c.operation == operation,
                request_logs.c.input_value == input_value,
                request_logs.c.result.isnot(None)
            )
            .limit(1)
        )
        return row is not None
