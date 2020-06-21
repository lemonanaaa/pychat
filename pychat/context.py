from typing import Tuple

from asyncio_dgram.aio import DatagramStream

from .proto import Message

SocketAddr = Tuple[str, int]


class Peer:
    stream: DatagramStream
    user_name: str = None
    addr: SocketAddr

    def __init__(self, stream: DatagramStream, addr: SocketAddr, user_name: str = None):
        self.stream = stream
        self.user_name = user_name
        self.addr = addr


class Context:
    peer: Peer

    def __init__(self, peer: Peer):
        self.peer = peer

    async def send(self, msg: Message):
        await self.peer.stream.send(msg.json().encode('utf-8'), addr=self.peer.addr)
