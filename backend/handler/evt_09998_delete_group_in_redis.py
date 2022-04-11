
from ducts.spi import EventHandler
import io
import pickle
import numpy as np
import pandas as pd
from scipy.io.wavfile import write
import soundfile as sf
import resampy

import logging
logger = logging.getLogger(__name__)

class Handler(EventHandler):

    def __init__(self):
        super().__init__()

    def setup(self, handler_spec, manager):
        self.evt_manipulate_redis = manager.get_handler_module('MANIPULATE_REDIS')
        self.evt_list_contents = manager.get_handler_module('BLOBS_CONTENT_LIST').list_contents
        handler_spec.set_description('UK Dissertation')
        return handler_spec

    async def handle(self, event):     
        return await self.call(**event.data)

    async def call(self, group_key: str):
        await self.delete_group(group_key)
        return {}

    async def delete_group(self, group_key: str):
        return await self.evt_manipulate_redis.delete_group(group_key, 'pkl')



