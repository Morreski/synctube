import logging
import argparse

import tornado
from tornado.httpserver import HTTPServer

from synctube.eventsources import HostEventStream
from synctube.sse_utils import AsyncioSSEHandler
from synctube import handlers
from synctube import views

parser = argparse.ArgumentParser()

parser.add_argument('--port', type=int,
                    help='The server listening port.',
                    default=4242)
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
        (r'^/player/(?P<player_id>[a-zA-Z0-9]*)$', views.PlayerPage),
        (r'^/player/(?P<player_id>[a-zA-Z0-9]*)/subscribe$', AsyncioSSEHandler, {'datasource': HostEventStream}),
        (r'^/player/(?P<player_id>[a-zA-Z0-9]*)/unsubscribe$', handlers.UnsubscribePlayer),

        (r'^/player/(?P<player_id>[a-zA-Z0-9]*)/play/(?P<video_id>.*)$', handlers.AddVideo),
        (r'^/player/(?P<player_id>[a-zA-Z0-9]*)/play$', handlers.CommandPlay),
        (r'^/player/(?P<player_id>[a-zA-Z0-9]*)/pause$', handlers.CommandPause),
        (r'^/player/(?P<player_id>[a-zA-Z0-9]*)/next', handlers.CommandNextSong),
        (r'^/player/(?P<player_id>[a-zA-Z0-9]*)/prev', handlers.CommandPrevSong),

        (r'^/player/(?P<player_id>[a-zA-Z0-9]*)/playlist/add/(?P<video_id>.*)$', handlers.AddVideoToPlaylist),
        (r'^/player/(?P<player_id>[a-zA-Z0-9]*)/playlist/next$', handlers.GetNextSongId),
        (r'^/player/(?P<player_id>[a-zA-Z0-9]*)/playlist/prev$', handlers.GetPreviousSongId),

        (r'^/controller/(?P<player_id>[a-zA-Z0-9]*)$', views.ControllerPage),

        (r'^/admin/drop-all$', handlers.DropAll),
        (r'^/admin/unsubscribe-all$', handlers.UnsubscribeAll),

        (r'/home$', views.HomePage),
        (r'^/$', tornado.web.RedirectHandler, {'url': '/home'}),
    ]
    return tornado.web.Application(routes,
                                   debug=debug,
                                   static_url_prefix='/static/',
                                   template_path='./templates',
                                   static_path='./static')


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
