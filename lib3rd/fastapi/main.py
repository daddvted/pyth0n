import time
import asyncio
import concurrent.futures
from typing import Optional
from fastapi import FastAPI

app = FastAPI()

loop = asyncio.get_running_loop()


def hello(name):
    time.sleep(10)
    return f"hello {name}"


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/hello/{name}")
async def read_item(name: Optional[str] = "Ted"):
    with concurrent.futures.ThreadPoolExecutor() as pool:
        result = await loop.run_in_executor(pool, hello, name)
    return result
