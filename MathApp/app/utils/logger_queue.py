import asyncio

log_queue: asyncio.Queue[str] = asyncio.Queue()
LOG_FILE = "logs.txt"


def init_log_file():
    with open(LOG_FILE, "w"):
        pass


async def send_log(message: str):
    await log_queue.put(message)


async def start_log_worker():
    while True:
        message = await log_queue.get()
        with open(LOG_FILE, "a") as f:
            f.write(message + "\n")
        log_queue.task_done()
