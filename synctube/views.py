import json

from tornado.web import RequestHandler

from synctube import shared
from synctube.player import PlayerEvent, Player


class HomePage(RequestHandler):

    async def get(self):
        self.render('index.html')


class PlaylistView(RequestHandler):

    async def get(self, player_id):
        if player_id not in shared.PLAYERS:
            self.send_error(404, reason='Player not found.')
            return
        self.write({'videos': list(shared.PLAYERS[player_id].playlist)})

    async def post(self, player_id):
        if player_id not in shared.PLAYERS:
            self.send_error(404, reason='Player not found.')
            return
        try:
            data = json.loads(self.request.body.decode())
            video_id = data['video_id']
        except json.JSONDecodeError as e:
            self.send_error(400, reason='Invalid JSON: %s.' % e)
            return
        except KeyError:
            self.send_error(400, reason='Missing "video_id" field in request.')
            return
        shared.PLAYERS[player_id].playlist.append(video_id)
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
