from tornado.web import RequestHandler

from synctube import shared


class CommandHandler(RequestHandler):

    ACTION_NAME = None

    async def get(self, player_id, video_id=None):
        if self.ACTION_NAME is None:
            raise NotImplementedError

        if player_id not in shared.EVENT_QUEUES:
            self.send_error(404)
            return

        shared.PLAYLISTS[player_id].insert_now(video_id)
        for conn_id in shared.EVENT_QUEUES[player_id]:
            await shared.EVENT_QUEUES[player_id][conn_id].put({
                'name': self.ACTION_NAME,
                'params': self.get_action_params(video_id)
            })

    def get_action_params(self, video_id):
        return dict()


class AddVideo(CommandHandler):
    ACTION_NAME = 'play_now'

    def get_action_params(self, video_id):
        return {
            'video_id': video_id
        }


class CommandPlay(CommandHandler):
    ACTION_NAME = 'play'


class CommandPause(CommandHandler):
    ACTION_NAME = 'pause'


class CommandNextSong(CommandHandler):
    ACTION_NAME = 'play_next'


class CommandPrevSong(CommandHandler):
    ACTION_NAME = 'play_prev'


class AddVideoToPlaylist(RequestHandler):

    async def get(self, player_id, video_id):
        if player_id not in shared.EVENT_QUEUES:
            self.send_error(404)
            return

        shared.PLAYLISTS[player_id].append(video_id)


class GetNextSongId(RequestHandler):

    async def get(self, player_id):
        if player_id not in shared.EVENT_QUEUES:
            self.send_error(404)
            return

        playlist = shared.PLAYLISTS[player_id]
        next_song_id = playlist.get_next_song()

        if next_song_id is None:
            self.send_error(416)
            return

        self.write(next_song_id)


class GetPreviousSongId(RequestHandler):

    async def get(self, player_id):
        if player_id not in shared.EVENT_QUEUES:
            self.send_error(404)
            return

        playlist = shared.PLAYLISTS[player_id]
        next_song_id = playlist.get_prev_song()

        if next_song_id is None:
            self.send_error(416)
            return

        self.write(next_song_id)


class UnsubscribePlayer(RequestHandler):

    async def get(self, player_id):
        if player_id not in shared.EVENT_QUEUES:
            self.send_error(404)
            return

        del shared.EVENT_QUEUES[player_id]


class DropAll(RequestHandler):

    async def get(self):
        shared.EVENT_QUEUES.clear()
        shared.PLAYLISTS.clear()
        shared.PLAYLISTS_POSITIONS.clear()


class UnsubscribeAll(RequestHandler):

    async def get(self):
        shared.EVENT_QUEUES.clear()
