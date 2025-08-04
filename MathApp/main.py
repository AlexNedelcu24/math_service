import uvicorn
import asyncio
from fastapi import FastAPI
from app.controllers.math_controller import router as math_router
from app.database.db import engine, metadata, database
from app.workers.worker import start_worker
from app.utils.logger_queue import start_log_worker, init_log_file
from contextlib import asynccontextmanager
from prometheus_fastapi_instrumentator import Instrumentator


@asynccontextmanager
async def lifespan(app: FastAPI):

    init_log_file()
    await database.connect()
    metadata.create_all(engine)

    worker_task = asyncio.create_task(start_worker())
    log_task = asyncio.create_task(start_log_worker())

    yield

    worker_task.cancel()
    log_task.cancel()
    await worker_task
    await log_task
    await database.disconnect()

app = FastAPI(title="MathService", lifespan=lifespan)
app.include_router(math_router)

Instrumentator().instrument(app).expose(app)

if __name__ == "__main__":
    uvicorn.run(
        "main:app", host="localhost", port=8000,
        reload=True, log_level="info",
    )
