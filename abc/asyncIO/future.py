import asyncio
import concurrent.futures


def blocking_io():
    # File operations(such as logging) can block the event loop:
    # run them in a thread pool.
    with open('/dev/urandom', 'rb') as f:
        return f.read(100)


def cpu_bound():
    # CPU-bound operations will block the event loop:
    # in general it is preferable to run them in a process pool.
    return sum(i * i for i in range(10 ** 7))

async def run_async_func(func, *args):
    loop = asyncio.get_running_loop()
    with concurrent.futures.ThreadPoolExecutor() as pool:
        return await loop.run_in_executor(pool, func, *args)


async def main():
    loop = asyncio.get_running_loop()
    ## Options:

    # 1. Run in the default loop's executor:
    result = await loop.run_in_executor(None, blocking_io)
    print('default thread pool', result)

    # 2. Run in a custom thread pool:
    result = await run_async_func(blocking_io)
    print('custom thread pool', result)

    # 3. Run in a custom process pool:
    with concurrent.futures.ProcessPoolExecutor() as pool:
        result = await loop.run_in_executor(pool, cpu_bound)
        print('custom process pool', result)


asyncio.run(main())
