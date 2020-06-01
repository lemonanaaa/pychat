from typing import Dict

from .member import Member
from ..context import Context
from ..handler import Handler
from .. import proto
import asyncio


class ChatRoom(Handler):
    name: str
    members: Dict[str, Member]
    creator_name: str

    def __init__(self, *, name: str, creator_name: str):
        self.members = {}
        self.name = name
        self.creator_name = creator_name

    def add_member(self, member: Member):
        self.members[member.name] = member

    async def handle_join_room(self, _ctx: Context, msg: proto.JoinRoom):
        await self.broadcast(msg)

    async def handle_send_message(self, _ctx: Context, msg: proto.SendMessage):
        await self.broadcast(msg)

    async def broadcast(self, msg: proto.Message):
        await asyncio.gather(*(member.send_message(msg) for member in self.members.values()))
