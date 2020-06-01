from pychat.client import ChatClient
import asyncio


async def main():
    client = ChatClient('Jack')
    await client.start()
    await client.create_room('test')
    await client.send_message('test', 'hello')


loop = asyncio.new_event_loop()
loop.run_until_complete(main())
loop.run_forever()
