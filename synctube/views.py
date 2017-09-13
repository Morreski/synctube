import json

from tornado.web import RequestHandler

from synctube import shared
from synctube.player import PlayerEvent


class HomePage(RequestHandler):

    async def get(self):
        self.render('index.html')


class PlayerPage(RequestHandler):

    async def get(self, player_id):
        self.render(
            'player.html',
            player_id=player_id
        )


class ControllerPage(RequestHandler):

    async def post(self, player_id):
        if player_id not in shared.PLAYERS:
            self.send_error(404)
            return
        try:
            event_dict = json.loads(self.request.body.decode())
            event = PlayerEvent(**event_dict)
        except json.JSONDecodeError as e:
            self.send_error(400, reason='Bad JSON: %s' % e)

        await shared.PLAYERS[player_id].add_event(event)

    async def get(self, player_id):
        if player_id not in shared.PLAYERS:
            self.send_error(404)
            return
        self.render(
            'controller.html',
            player_id=player_id
        )
