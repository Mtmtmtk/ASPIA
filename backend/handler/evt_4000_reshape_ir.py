from ducts.spi import EventHandler
import numpy as np
import pandas as pd
from matplotlib import pyplot
import logging
logger = logging.getLogger(__name__)

class Handler(EventHandler):

    def __init__(self):
        super().__init__()

    def setup(self, handler_spec, manager):
        handler_spec.set_description('UK Dissertation')
        return handler_spec

    async def handle(self, event):     
        return {}

    async def call(self, ir_arr, spl_rate: int, channels:int):
        sr_ir = pd.Series(ir_arr)
        sr_ir = sr_ir/sr_ir.max()
        signal_per_channel = sr_ir[sr_ir.index % channels == 0].reset_index(drop=True)

        col_name = [f'channel_{i}' for i in range(channels)]
        for ind in range(channels):
            if ind != 0:
                signal_per_channel = pd.concat([signal_per_channel, sr_ir[sr_ir.index % channels == ind].reset_index(drop=True)], axis=1)
        
        signal_per_channel.columns = col_name

        signal_per_channel['time_stamp'] = signal_per_channel.index / spl_rate
        return signal_per_channel
