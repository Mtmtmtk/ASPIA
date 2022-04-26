from enum import IntEnum
from ducts.spi import EventHandler, webapi

import logging
logger = logging.getLogger(__name__)

class ForecastStatus(IntEnum):
    IDLE                    = 100
    IN_DOWNLOAD             = 110
    DOWNLOAD_FINISHED       = 200
    ANECHOIC_SOUND_FINISHED = 210
    IN_IR_IMPORT            = 220
    IN_RESAMPLE             = 230
    IN_CONVOLUTIOM          = 240
    FINISHED_PROCESS        = 300

class Hander(EventHandler):
    def __init__(self):
        super().__init__()

    def setup(self, handler_spec, manager):
        self.redis = manager.redis
        handler_spec.set_description('')
        return handler_spec

    async def run(self, manager):
        if not await self.get():
            await self.set(ForecastStatus.IDLE)

    async def handle(self, event):
        pass

    def pubsubkey(self, username="default"):
        return f"{username}/ForecastStatus/PubSubKey"
    def streamkey(self, username="default"):
        return f"{username}/ForecastStatus"

    async def list(self):
        return { s.name: s.value for s in ForecastStatus }

    async def get(self):
        status_rec = await self.redis.xlast_str(self.streamkey())
        return status_rec["Status"] if status_rec else None

    async def set(self, status):
        status = status.value if isinstance(status, ForecastStatus) else status

        await self.redis.xadd_and_publish(
            self.pubsubkey(),
            self.streamkey(),
            Status=status)

    @webapi.add_route(path="/set/{status}", method="*")
    async def set_api(self, request):
        status = request.match_info["status"]
        await self.set(status)
        return web.json_response({})

    async def watch(self):
        ch = await self.redis.psubscribe(self.pubsubkey())
        yield await self.get()
        async for msg in ch.iter():
            stream_id = msg[1]
            status_rec = await self.redis.xget_str(self.streamkey(), stream_id)
            yield status_rec["Status"]

