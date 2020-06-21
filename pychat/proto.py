from typing import Optional

import orjson
from pydantic import BaseModel, ValidationError


class Message(BaseModel):
    type: str


class SignUp(Message):
    type = 'signup'
    signup_name: str
    signup_password: str


class Login(Message):
    type = 'login'
    login_name: str
    login_password: str


class LoginResponse(Message):
    type = 'login_response'
    success: bool
    id: Optional[int] = None


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
    'send_message': SendMessage,
    'login': Login,
    'signup': SignUp,
    'login_response': LoginResponse
}


def parse_message(msg: bytes) -> Optional[Message]:
    try:
        data = orjson.loads(msg)
        return _MESSAGE_MAP[data['type']](**data)
    except (orjson.JSONDecodeError, ValidationError):
        return None
