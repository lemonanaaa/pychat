from asyncio import StreamWriter
from ..proto import Message


class Member:
    name: str
    writer: StreamWriter

    def __init__(self, name: str, writer: StreamWriter):
        self.name = name
        self.writer = writer

    async def send_message(self, msg: Message):
        self.writer.write(msg.json().encode(encoding='utf8'))
        await self.writer.drain()
