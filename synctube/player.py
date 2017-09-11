from collections import namedtuple
import asyncio

from synctube.playlist import Playlist

PlayerEvent = namedtuple('PlayerEvent', ['type', 'data'])


class Player:

    def __init__(self, id_):
        self._id = id_
        self._event_stream = asyncio.queues.Queue()
        self.playlist = Playlist()

    async def add_event(self, event):
        await self._event_stream.put(event)

    async def poll_event(self):
        return await self._event_stream.get()
