from collections import namedtuple, defaultdict
import asyncio

PlayerEvent = namedtuple('PlayerEvent', ['type', 'data'])


class Player:

    def __init__(self, id_):
        self._id = id_
        self._event_stream = asyncio.queues.Queue()
        self._playlist = Playlist()

    async def add_event(self, event):
        await self._event_stream.put(event)

    async def poll_event(self):
        return await self._event_stream.get()


class Playlist:

    def __init__(self):
        keys = ['next', 'prev']
        self._videos = defaultdict(lambda: dict.fromkeys(keys))
        self.currently_playing = None
        self.last = None
        self.first = None

    def append(self, video_id):
        if video_id in self._videos:
            return  # Video already here, do nothing to avoid duplicates

        if self.first is None:
            self.first = video_id
            self._videos[video_id]['next'] = None
            self._videos[video_id]['prev'] = None
        else:
            self._videos[self.last]['next'] = video_id
            self._videos[video_id]['prev'] = self.last

        self.last = video_id

    def insert_now(self, video_id):
        if video_id in self._videos:
            return  # Video already here, do nothing to avoid duplicates

        if self.first is None:
            self.append(video_id)
            return

        if self.currently_playing is not None:
            next_video = self._videos[self.currently_playing]['next']
        else:
            next_video = self.first

        if next_video is None:
            self.last = video_id
        else:
            self._videos[next_video]['prev'] = video_id

        self._videos[self.currently_playing]['next'] = video_id
        self._videos[video_id]['prev'] = self.currently_playing
        self._videos[video_id]['next'] = next_video
        self.currently_playing = video_id

    def get_next_song(self):
        if self.currently_playing is None:
            self.currently_playing = self.first
            return self.first
        next_video = self._videos[self.currently_playing]['next']

        if next_video is None:
            return None

        self.currently_playing = next_video
        return self.currently_playing

    def get_prev_song(self):
        if self.currently_playing is None:
            return None
        self.currently_playing = self._videos[self.currently_playing]['prev']
        return self.currently_playing
