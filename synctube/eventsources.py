import json

from synctube.sse_utils import DataSource, SSEError
from synctube import shared


class PlayerEventStream(DataSource):

    async def before(self):
        player_id = self.args['player_id']
        try:
            self.event_source = shared.PLAYERS[player_id].subscribe()
        except KeyError:
            raise SSEError(404, 'Player not found.')

    async def loop(self):
        evt = await self.event_source.get()
        return json.dumps(evt.data), evt.type, self.current_iteration
