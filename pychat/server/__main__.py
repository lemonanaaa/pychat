import asyncio

from pychat.server import ChatServer


async def main():
    server = ChatServer()
    print('chat server listening')
    await server.start()


asyncio.run(main())
