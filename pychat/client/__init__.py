import asyncio
from .. import proto
from ..context import Context
from ..handler import Handler


class ChatClient(Handler):
    user_name: str
    reader: asyncio.StreamReader
    writer: asyncio.StreamWriter

    def __init__(self, user_name: str):
        self.user_name = user_name

    async def start(self):
        self.reader, self.writer = await asyncio.open_connection('127.0.0.1', 8888)

        async def listen():
            data = b''
            ctx = Context(reader=self.reader, writer=self.writer)
            while True:
                data = data + await self.reader.read(100)
                if (msg := proto.parse_message(data)) is not None:
                    await self.handle_message(ctx, msg)
                    data = b''

        asyncio.create_task(listen())

    async def send_message(self, room_name: str, content: str):
        await self.write(proto.SendMessage(room_name=room_name, creator_name=self.user_name, msg=content))

    async def create_room(self, room_name: str):
        await self.write(proto.CreateRoom(room_name=room_name, creator_name=self.user_name))

    async def join_room(self, room_name: str):
        await self.write(proto.JoinRoom(room_name=room_name, user_name=self.user_name))

    async def handle_join_room(self, _ctx: Context, msg: proto.JoinRoom):
        print(f'Room[{msg.room_name}]: {msg.user_name} joined')

    async def handle_send_message(self, _ctx: Context, msg: proto.SendMessage):
        print(f'Room[{msg.room_name}][{msg.creator_name}]: {msg.msg}')

    async def write(self, msg: proto.Message):
        self.writer.write(msg.json().encode(encoding='utf8'))
        await self.writer.drain()
