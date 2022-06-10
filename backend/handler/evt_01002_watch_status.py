from ducts.spi import EventHandler

import logging
logger = logging.getLogger(__name__)

class Handler(EventHandler):

    def __init__(self):
        super().__init__()

    def setup(self, handler_spec, manager):
        self.evt_status = manager.get_handler_for(manager.key_ids["STATUS"])[1]
        handler_spec.set_description('')
        return handler_spec

    async def handle(self, event):
        async for status in self.evt_status.watch():
            yield status
