from ..context import Peer
from ..proto import Message


class Member:
    name: str
    peer: Peer

    def __init__(self, name: str, peer: Peer):
        self.name = name
        self.peer = peer

    async def send_message(self, msg: Message):
        await self.peer.stream.send(msg.json().encode(encoding='utf8'), addr=self.peer.addr)
