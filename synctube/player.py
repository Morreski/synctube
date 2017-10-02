from collections import namedtuple, defaultdict
import asyncio

PlayerEvent = namedtuple('PlayerEvent', ['type', 'data'])


class PlaylistError(Exception):
    pass


class Player:

    def __init__(self, id_, max_event_stream_size=100):
        self._id = id_
        self.playlist = Playlist()
        self.position_in_playlist = None
        self._subscriptions = list()

    async def add_event(self, event):
        self.run_hook(event)
        for subscription in self._subscriptions:
            await subscription.put(event)

    def subscribe(self):
        subscription = asyncio.queues.Queue()
        self._subscriptions.append(subscription)
        return subscription

    def get_navigation(self):
        if self.position_in_playlist is None:
            return {'prev': None, 'next': self.playlist.first}
        return self.playlist[self.position_in_playlist]

    def run_hook(self, event):
        event_type = event.type
        hook = getattr(self, 'hook_' + event_type, None)
        if hook is not None:
            hook(event)

    def hook_play_next(self, event):
        pos = self.position_in_playlist
        if pos is None:
            next_song = self.playlist.first
        else:
            next_song = self.playlist[pos]['next']
        self.position_in_playlist = next_song

    def hook_play_prev(self, event):
        pos = self.position_in_playlist
        if pos is None:
            prev_song = None
        else:
            prev_song = self.playlist[pos]['prev']
        self.position_in_playlist = prev_song


class Playlist:

    def __init__(self):
        self._videos = defaultdict(lambda: dict.fromkeys(('next', 'prev')))
        self.last = None
        self.first = None

    def __getitem__(self, video_id):
        return self._videos[video_id]

    def __iter__(self):
        video_id = self.first
        while video_id is not None:
            yield video_id
            video_id = self[video_id]['next']

    def append(self, video_id):
        if video_id in self._videos:
            raise PlaylistError('Video is already in playlist.')

        if self.first is None:
            self.first = video_id
            self[video_id]['next'] = None
            self[video_id]['prev'] = None
        else:
            self[self.last]['next'] = video_id
            self[video_id]['prev'] = self.last

        self.last = video_id

    def insert_after(self, after_id, video_id):
        if video_id in self._videos:
            raise PlaylistError('Video is already in playlist.')
        if after_id not in self._videos:
            raise PlaylistError('Cannot insert video: %s not in playlist.' % after_id)
        left_video = self[after_id]
        right_video_id = left_video['next']
        self[right_video_id]['prev'] = video_id
        left_video['next'] = video_id
        self[video_id]['next'] = right_video_id
        self[video_id]['prev'] = after_id
