# Run code async code using asyncio Tasks
import asyncio
import time


async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)


async def main():
    task1 = asyncio.create_task(
        say_after(3, 'hello')
    )

    task2 = asyncio.create_task(
        say_after(6, 'world')
    )
    print(f"started at {time.strftime('%X')}")

    await task1
    await task2

    print(f"finished at {time.strftime('%X')}")

asyncio.run(main())