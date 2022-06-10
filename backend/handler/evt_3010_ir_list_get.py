from ducts.spi import EventHandler
import os
import glob
import logging
logger = logging.getLogger(__name__)

class Handler(EventHandler):

    def __init__(self):
        super().__init__()

    def setup(self, handler_spec, manager):
        handler_spec.set_description('UK Dissertation')
        return handler_spec

    async def handle(self, event):     
        return await self.call(**event.data)

    async def call(self, abbr:str, audioType:str):
        path = './impulse_response/' + abbr + '/' + audioType
        files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        return files
