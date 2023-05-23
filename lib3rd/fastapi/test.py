import functools
from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import JSONResponse

def cached(key: str = ""):
    def wrapper(func):

        @functools.wraps(func)
        def wrapper_for_func(*args, **kwargs):
            # Hijack trick happens HERE
            if key:
                print("000")
                return key
            else:
                print("111")
                print(args)
                print(kwargs)
                return func(*args, **kwargs)

        return wrapper_for_func

    return wrapper

app = FastAPI()

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    u = str(request.url)
    if u.endswith('coffee'):
        d = {"mother": "fucker"}
        resp = JSONResponse(d)
        return resp

    print(f'------------- {request.url}')
    response = await call_next(request)
    print(response)
    return response


@app.get("/{drink}")
async def root(drink: str):
    print('ymd')
    return {"message": f"{drink}"}