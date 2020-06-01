from pychat.server import ChatServer
import asyncio


async def main():
    server = ChatServer()
    print('chat server listening at 127.0.0.1:8888')
    await server.start()


asyncio.run(main())
