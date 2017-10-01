import asyncio

from tornado.web import RequestHandler


class SSEError(Exception):

    def __init__(self, code, reason):
        self.reason = reason
        self.code = code

    def __str__(self):
        return '<%d>: %s' % (self.code, self.reason)


class DataSource:

    def __init__(self, max_iterations=1, forever=False, **kwargs):
        self.args = kwargs
        self.max_iterations = max_iterations
        self.forever = forever
        self.current_iteration = 0

    async def __aiter__(self):
        return self

    async def before(self):
        pass

    async def after(self):
        pass

    async def __anext__(self):
        self.current_iteration += 1
        if self.current_iteration <= self.max_iterations or self.forever:
            yielded = await self.loop()
            return yielded
        raise StopAsyncIteration

    async def loop(self):
        raise NotImplementedError


class AsyncioSSEHandler(RequestHandler):

    def initialize(self, datasource, freq=0):
        self.datasource = datasource
        self.freq = freq
        self.set_header('Content-Type', 'text/event-stream')
        self.set_header('Cache-Control', 'no-cache/no-store')

    async def publish(self, response, event_type, event_id):

        if event_type is not None:
            self.write('event: %s\n' % event_type)
        if event_id is not None:
            self.write('id: %d\n' % event_id)

        self.write('data: %s\n\n' % response)
        self.flush()

    async def get(self, **kwargs):
        datasource = self.datasource(forever=True, **kwargs)
        try:
            await datasource.before()
        except SSEError as e:
            self.send_error(e.code, reason=e.reason)
            return
        async for data in datasource:
            await self.publish(*data)
            if self.freq > 0:
                await asyncio.sleep(1 / self.freq)
        await datasource.after()
