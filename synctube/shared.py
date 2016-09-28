from collections import defaultdict
import asyncio

from synctube.playlist import Playlist


def _create_connection_queue():
    return defaultdict(lambda: asyncio.queues.Queue())

EVENT_QUEUES = defaultdict(_create_connection_queue)
PLAYLISTS = defaultdict(lambda: Playlist())
