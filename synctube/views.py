import json

from tornado.web import RequestHandler

from synctube import shared
from synctube.player import PlayerEvent, Player, PlaylistError


class HomePage(RequestHandler):

    async def get(self):
        self.render('index.html')


class PlaylistView(RequestHandler):

    async def get(self, player_id):
        if player_id not in shared.PLAYERS:
            self.send_error(404, reason='Player not found.')
            return
        player = shared.PLAYERS[player_id]
        self.write({
            'videos': list(player.playlist),
            'navigation': player.get_navigation(),
            'currently_playing': player.position_in_playlist,
        })

    async def post(self, player_id):
        if player_id not in shared.PLAYERS:
            self.send_error(404, reason='Player not found.')
            return
        try:
            data = json.loads(self.request.body.decode())
            video_id = data['video_id']
            after_id = data.get('insert_after')
        except json.JSONDecodeError as e:
            self.send_error(400, reason='Invalid JSON: %s.' % e)
            return
        except KeyError as e:
            self.send_error(400, reason='Field is required: %s.' % e)
            return
        try:
            if after_id is None:
                shared.PLAYERS[player_id].playlist.append(video_id)
            else:
                shared.PLAYERS[player_id].playlist.insert_after(after_id, video_id)
        except PlaylistError as e:
            self.send_error(400, reason=str(e))

        event = PlayerEvent(data={}, type='playlistUpdated')
        await shared.PLAYERS[player_id].add_event(event)


class PlayerView(RequestHandler):

    async def get(self, player_id):
        if player_id not in shared.PLAYERS:
            self.send_error(404, reason='Player not found.')
            return
        self.render(
            'player.html',
            player_id=player_id
        )

    async def post(self, player_id):
        if player_id in shared.PLAYERS:
            self.send_error(400, reason='Player already exists.')
            return
        player = Player(player_id)
        shared.PLAYERS[player_id] = player

    async def delete(self, player_id):
        if player_id not in shared.PLAYERS:
            self.send_error(404, reason='Player not found.')
            return
        player = Player(player_id)
        shared.PLAYERS[player_id] = player


class ControllerView(RequestHandler):

    async def post(self, player_id):
        if player_id not in shared.PLAYERS:
            self.send_error(404, reason='Player not found.')
            return
        try:
            event_dict = json.loads(self.request.body.decode())
            event = PlayerEvent(**event_dict)
        except json.JSONDecodeError as e:
            self.send_error(400, reason='Invalid JSON: %s.' % e)

        await shared.PLAYERS[player_id].add_event(event)

    async def get(self, player_id):
        if player_id not in shared.PLAYERS:
            self.send_error(404, reason='Player not found.')
            return
        self.render(
            'controller.html',
            player_id=player_id
        )
