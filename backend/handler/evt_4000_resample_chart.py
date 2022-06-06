from ducts.spi import EventHandler
import numpy as np
import pandas as pd
import logging
import resampy
logger = logging.getLogger(__name__)

class Handler(EventHandler):

    def __init__(self):
        super().__init__()

    def setup(self, handler_spec, manager):
        handler_spec.set_description('UK Dissertation')
        try:
            self.evt_load_data = manager.get_handler_module('LOAD_DATA_FROM_REDIS')
        except Exception as e:
            import traceback
            traceback.print_exc()
        return handler_spec

    async def handle(self, event):     
        return {}

    async def call(self, group_key: str):
        df = await self.evt_load_data.load_group_data(group_key)
        df_resampled = pd.DataFrame(columns=df.columns)
        for i in df.columns:
            arr = df.iloc[:,i].values
            arr_resampled = resampy.resample(arr, 44100, 44100/10)
            df_resampled.iloc[:,i] = arr_resampled
        df_resampled = df_resampled / df_resampled.abs().max(axis=0).max(axis=0)
        
        ir_bigger = df_resampled.max(axis=1)
        offset_ind = ir_bigger[ir_bigger > 0.05].index[0] - 1
        df_resampled = df_resampled.drop(index=df_resampled.index[:offset_ind])
        df_resampled = df_resampled.reset_index(drop=True)

        sr_time_stamp = pd.Series(df_resampled.index/(44100/10))
        sr_time_stamp = sr_time_stamp.round(2)
        return [ df_resampled, sr_time_stamp ]
