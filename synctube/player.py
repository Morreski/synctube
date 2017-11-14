from collections import namedtuple, defaultdict
import asyncio

from synctube.hooks import hook_play_next, hook_play_prev

PlayerEvent = namedtuple('PlayerEvent', ['type', 'data'])


class PlaylistError(Exception):
    pass


class Player:

    DEFAULT_HOOKS = {
        'play_next': [hook_play_next],
        'play_prev': [hook_play_prev]
    }

    def __init__(self, id_, max_event_stream_size=100, hooks={}):
        self._id = id_
        self.playlist = Playlist()
        self.position_in_playlist = None
        self._subscriptions = list()
        self._hooks = hooks or self._init_hooks()

    async def add_event(self, event):
        self.run_hook(event)
        for subscription in self._subscriptions:
            await subscription.put(event)

    def _init_hooks(self):
        return self.DEFAULT_HOOKS.copy()

    def add_hook(self, event_type, hook_func):
        if not callable(hook_func):
            raise TypeError('hook_func must be callable.')
        self._hooks[event_type] = hook_func

    def remove_hook(self, event_type):
        del self._hooks[event_type]

    @property
    def hook(self):
        return self._hooks

    def subscribe(self):
        subscription = asyncio.queues.Queue()
        self._subscriptions.append(subscription)
        return subscription

    def get_navigation(self):
        if self.position_in_playlist is None:
            return {'prev': None, 'next': self.playlist.first}
        return self.playlist[self.position_in_playlist]

    def run_hook(self, event):
        for hook in self._hooks.get(event.type, []):
            hook(self, event)


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
