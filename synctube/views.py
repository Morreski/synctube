import json

from tornado.web import RequestHandler

from synctube import shared
from synctube.player import PlayerEvent, Player


class HomePage(RequestHandler):

    async def get(self):
        self.render('index.html')


class PlayerView(RequestHandler):

    async def get(self, player_id):
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
            self.send_error(404, 'Player not found.')
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
