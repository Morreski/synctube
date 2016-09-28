import json
import uuid

from synctube.sse_utils import DataSource
from synctube import shared


class HostEventStream(DataSource):

    async def before(self):
        self.connection_id = uuid.uuid4().hex

    async def loop(self):
        player_id = self.args['player_id']
        event = await shared.EVENT_QUEUES[player_id][self.connection_id].get()
        response = json.dumps(event['params'])
        return response, event['name'], self.current_iteration
