from pydantic import BaseModel, ValidationError
import orjson
from typing import Optional


class Message(BaseModel):
    type: str


class JoinRoom(Message):
    type: str = 'join_room'
    room_name: str
    user_name: str


class CreateRoom(Message):
    type: str = 'create_room'
    room_name: str
    creator_name: str


class SendMessage(Message):
    type: str = 'send_message'
    room_name: str
    creator_name: str
    msg: str


_MESSAGE_MAP = {
    'join_room': JoinRoom,
    'create_room': CreateRoom,
    'send_message': SendMessage
}


def parse_message(msg: bytes) -> Optional[Message]:
    try:
        data = orjson.loads(msg)
        return _MESSAGE_MAP[data['type']](**data)
    except (orjson.JSONDecodeError, ValidationError):
        return None
