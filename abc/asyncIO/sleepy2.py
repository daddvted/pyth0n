import time
from typing import Optional
from fastapi import FastAPI

app = FastAPI()


@app.get("/sleepy")
async def sleepy(sec: Optional[int] = 2):
    time.sleep(sec)
    return f"done(sleep for {sec}s)"
