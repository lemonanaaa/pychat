from asyncio import StreamWriter, StreamReader


class Context:
    reader: StreamReader
    writer: StreamWriter

    def __init__(self, reader: StreamReader, writer: StreamWriter):
        self.reader = reader
        self.writer = writer
