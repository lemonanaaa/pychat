import asyncio

from .member import Member
from ..handler import Handler
from .. import proto
from ..context import Context
from typing import Dict
from .room import ChatRoom


class ChatServer(Handler):
    rooms: Dict[str, ChatRoom]
    server: asyncio.AbstractServer

    def __init__(self):
        self.rooms = {}

    async def start(self):
        self.server = await asyncio.start_server(self._serve, '127.0.0.1', 8888)
        async with self.server:
            await self.server.serve_forever()

    async def _serve(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        data = b''
        ctx = Context(reader=reader, writer=writer)
        while True:
            # FIXME: 这里有bug, TCP是字节流需要自己分割包
            data = data + await reader.read(100)
            print(data)
            if (msg := proto.parse_message(data)) is not None:
                print(msg.json())
                asyncio.create_task(self.handle_message(ctx, msg))
                data = b''

    async def handle_join_room(self, ctx: Context, msg: proto.JoinRoom):
        if (chat_room := self.rooms.get(msg.room_name, None)) is None:
            return
        chat_room.add_member(Member(name=msg.user_name, writer=ctx.writer))
        return await chat_room.handle_message(ctx, msg)

    async def handle_create_room(self, ctx: Context, msg: proto.CreateRoom):
        chat_room = ChatRoom(name=msg.room_name, creator_name=msg.creator_name)
        chat_room.add_member(Member(name=msg.creator_name, writer=ctx.writer))
        self.rooms[chat_room.name] = chat_room

    async def handle_send_message(self, ctx: Context, msg: proto.SendMessage):
        if (chat_room := self.rooms.get(msg.room_name, None)) is None:
            return
        return await chat_room.handle_message(ctx, msg)
