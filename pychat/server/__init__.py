import asyncio
from typing import Dict

import asyncio_dgram

from .member import Member
from .room import ChatRoom
from .. import proto
from ..context import Context, Peer, SocketAddr
from ..crud.models import User
from ..handler import Handler


class ChatServer(Handler):
    rooms: Dict[str, ChatRoom]
    server: asyncio.AbstractServer
    peers: Dict[SocketAddr, Peer]

    def __init__(self):
        self.rooms = {}
        self.peers = {}

    async def start(self):
        server = await asyncio_dgram.bind(('192.168.1.10', 9999))
        while True:
            data, addr = await server.recv()
            print(data, addr)
            if (peer := self.peers.get(addr, None)) is None:
                peer = Peer(stream=server, addr=addr)
                self.peers[addr] = peer
            ctx = Context(peer=peer)
            if (msg := proto.parse_message(data)) is not None:
                asyncio.create_task(self.handle_message(ctx, msg))

    async def handle_join_room(self, ctx: Context, msg: proto.JoinRoom):
        if (chat_room := self.rooms.get(msg.room_name, None)) is None:
            return
        chat_room.add_member(Member(name=msg.user_name, peer=ctx.peer))
        return await chat_room.handle_message(ctx, msg)

    async def handle_create_room(self, ctx: Context, msg: proto.CreateRoom):
        chat_room = ChatRoom(name=msg.room_name, creator_name=msg.creator_name)
        chat_room.add_member(Member(name=msg.creator_name, peer=ctx.peer))
        self.rooms[chat_room.name] = chat_room

    async def handle_send_message(self, ctx: Context, msg: proto.SendMessage):
        if (chat_room := self.rooms.get(msg.room_name, None)) is None:
            return
        return await chat_room.handle_message(ctx, msg)

    async def handle_signup(self, _ctx: Context, msg: proto.SignUp):  # noqa
        await User.create(name=msg.signup_name, password=msg.signup_password)

    async def handle_login(self, ctx: Context, msg: proto.Login):  # noqa
        user = await User.filter(name=msg.login_name, password=msg.login_password).first()
        if user is None:
            await ctx.send(proto.LoginResponse(success=False))
        else:
            await ctx.send(proto.LoginResponse(success=True, id=user.id))
