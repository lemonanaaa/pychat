import asyncio

from aioconsole import ainput

from pychat.client import ChatClient


async def main():
    client = ChatClient('Jack')
    await client.start()
    await client.create_room('test')
    await client.send_message('test', 'hello')

    while True:
        msg = await ainput()
        await client.send_message('test', msg)


loop = asyncio.new_event_loop()
loop.run_until_complete(main())
loop.run_forever()
