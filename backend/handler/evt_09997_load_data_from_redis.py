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
        ret = await self.load_group_data(group_key)
        return ret

    async def load_group_data(self, group_key: str):
        contents_list = await self.evt_list_contents(group_key, 'pkl')
        concat_df = pd.DataFrame(index=[])
        for content_key in contents_list:
            ret_df = await self.evt_manipulate_redis.load_dataframe_by_frame(group_key, content_key, '', 'pkl')
            concat_df = pd.concat([concat_df,ret_df])
        concat_df = concat_df.reset_index(drop=True)
        return concat_df

