import asyncio


async def netsted():
    return 36


async def main():
    netsted()

    print(await netsted())


asyncio.run(main())
