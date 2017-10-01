import os
import logging
import argparse

import tornado
from tornado.httpserver import HTTPServer

from synctube.eventsources import PlayerEventStream
from synctube.sse_utils import AsyncioSSEHandler
from synctube import views

BASE = os.path.dirname(__file__)

parser = argparse.ArgumentParser()

parser.add_argument('--port', type=int,
                    help='The server listening port. (default to 8080)',
                    default=8080)
parser.add_argument('--logfile', type=str,
                    help='Path for the logfile. If not specified, server will print to stdout.',
                    default='')
parser.add_argument('-v', '--verbose',
                    help='Talkative server.',
                    action='store_true')
parser.add_argument('--debug',
                    help='Start server in debug mode.',
                    action='store_true')


def make_app(debug=True):
    routes = [
        (r'/home$', views.HomePage),
        (r'^/$', tornado.web.RedirectHandler, {'url': '/home'}),
        (r'^/player/(?P<player_id>[a-zA-Z0-9]*)$', views.PlayerView),
        (r'^/player/(?P<player_id>[a-zA-Z0-9]*)/subscribe$', AsyncioSSEHandler, {'datasource': PlayerEventStream}),
        (r'^/controller/(?P<player_id>[a-zA-Z0-9]*)$', views.ControllerView),
        (r'^/playlist/(?P<player_id>[a-zA-Z0-9]*)$', views.PlaylistView),
    ]
    return tornado.web.Application(routes,
                                   debug=debug,
                                   static_url_prefix='/static/',
                                   template_path=os.path.join(BASE, 'templates'),
                                   static_path=os.path.join(BASE, 'static'))


def main():
    args = parser.parse_args()
    # Logging setup
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.getLogger().setLevel(log_level)
    params = {'format': '%(asctime)s:%(levelname)s:%(message)s'}
    params['filename'] = args.logfile
    logging.basicConfig(**params)

    # HTTP Server setup
    tornado.platform.asyncio.AsyncIOMainLoop().install()  # Use asyncio event loop instead of tornado ioloop.
    http_server = HTTPServer(
        make_app(args.debug),
    )
    http_server.listen(args.port)

    logging.info('Starting HTTP server on port: %d.' % args.port)
    if args.debug:
        logging.warning('Server started in debug mode.')

    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    main()
