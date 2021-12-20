from asyncio import sleep


async def run(client):
    while True:
        await sleep(10)
        body = {"lol": "DEEZ NUTS"}
        await client._add_to_queue(body)
