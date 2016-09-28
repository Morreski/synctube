from tornado.web import RequestHandler

from synctube import shared


class HomePage(RequestHandler):

    async def get(self):
        self.render('index.html')


class PlayerPage(RequestHandler):

    async def get(self, player_id):
        self.render('player.html',
                    player_id=player_id)


class ControllerPage(RequestHandler):

    async def get(self, player_id):
        if player_id not in shared.EVENT_QUEUES:
            self.send_error(404)
            return
        self.render('controller.html',
                    player_id=player_id)
