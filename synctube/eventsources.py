import json

from synctube.sse_utils import DataSource
from synctube import shared


class PlayerEventStream(DataSource):

    async def loop(self):
        player_id = self.args['player_id']
        evt = await shared.PLAYERS[player_id].poll_event()
        return json.dumps(evt.data), evt.type, self.current_iteration
