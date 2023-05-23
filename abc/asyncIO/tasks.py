import asyncio


async def nested():
    return 36


async def main():
    task = asyncio.create_task(nested())
    await task


asyncio.run(main())
