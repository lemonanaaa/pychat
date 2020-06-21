import asyncio

import asyncio_dgram
from aioconsole import aprint

from .. import proto
from ..context import Context, Peer
from ..handler import Handler


class ChatClient(Handler):
    user_name: str
    peer: Peer
    is_logged_in = False
    user_id: int = None

    def __init__(self, user_name: str):
        self.user_name = user_name

    async def start(self):
        addr = ('192.168.1.10', 9999)
        stream = await asyncio_dgram.connect(addr)
        self.peer = Peer(stream=stream, addr=addr)
        ctx = Context(peer=self.peer)

        async def listen():
            while True:
                data, _ = await stream.recv()
                if (msg := proto.parse_message(data)) is not None:
                    await self.handle_message(ctx, msg)

        asyncio.create_task(listen())

    async def send_message(self, room_name: str, content: str):
        await self.send(proto.SendMessage(room_name=room_name, creator_name=self.user_name, msg=content))

    async def create_room(self, room_name: str):
        await self.send(proto.CreateRoom(room_name=room_name, creator_name=self.user_name))

    async def join_room(self, room_name: str):
        await self.send(proto.JoinRoom(room_name=room_name, user_name=self.user_name))

    async def signup(self, name: str, password: str):
        await self.send(proto.SignUp(signup_name=name, signup_password=password))

    async def login(self, name: str, password: str):
        await self.send(proto.Login(login_name=name, login_password=password))

    async def handle_join_room(self, _ctx: Context, msg: proto.JoinRoom):  # noqa
        await aprint(f'Room[{msg.room_name}]: {msg.user_name} joined\n>>>', end='')

    async def handle_send_message(self, _ctx: Context, msg: proto.SendMessage):  # noqa
        await aprint(f'Room[{msg.room_name}][{msg.creator_name}]: {msg.msg}\n>>>', end='')

    async def handle_login_response(self, _ctx: Context, msg: proto.LoginResponse):
        self.is_logged_in = msg.success
        if msg.success:
            self.user_id = msg.id

    async def send(self, msg: proto.Message):
        await self.peer.stream.send(msg.json().encode(encoding='utf8'))
