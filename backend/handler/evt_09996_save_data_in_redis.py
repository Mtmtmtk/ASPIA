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
        handler_spec.set_description('UK Dissertation')
        return handler_spec

    async def handle(self, event):     
        return await self.call(**event.data)

    async def call(self, frame_no: int, group_key: str, data: list):
        await self.save_data(frame_no, group_key, data)
        return 'finished'

    async def save_data(self, frame_no: int, group_key: str, data:list):
        np_data = np.array(data)
        if len(data) == 1:
            np_data = np_data.flatten()
        df = pd.DataFrame(np_data.T)
        return await self.evt_manipulate_redis.save_dataframe_by_frame(frame_no, group_key, df, 'pkl')

