from ducts.spi import EventHandler
import numpy as np
import pandas as pd
import logging
logger = logging.getLogger(__name__)

class Handler(EventHandler):

    def __init__(self):
        super().__init__()

    def setup(self, handler_spec, manager):
        handler_spec.set_description('UK Dissertation')
        self.evt_resample_chart = manager.get_handler_module('RESAMPLE_CHART')
        return handler_spec

    async def handle(self, event):     
        return await self.call(**event.data)

    async def call(self, group_key: str):
        [ resampled_df, time_stamp ]  = await self.evt_resample_chart.call(group_key)
        return [ resampled_df.T.to_numpy().tolist(), time_stamp.tolist() ]
