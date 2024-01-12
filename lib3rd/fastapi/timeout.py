import time
import asyncio
from fastapi import FastAPI, Request

app = FastAPI()

@app.get("/")
def get_func():
    return  "hello"

@app.get("/sleep")
async def index():
    await asyncio.sleep(6)
    return "sleep"
