from .proto import Message
from .context import Context


class Handler:
    async def handle_message(self, ctx: Context, msg: Message):
        handler = getattr(self, f'handle_{msg.type}', None)
        if handler is None:
            raise ValueError(f'{msg.type} message not supported')
        return await handler(ctx, msg)
