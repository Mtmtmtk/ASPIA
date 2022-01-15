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
        self.evt_resample_ir_chart = manager.get_handler_module('RESAMPLE_IR_CHART')
        return handler_spec

    async def handle(self, event):     
        return await self.call(**event.data)

    async def call(self, ir_arr):
        [ resampled_ir, time_stamp ]  = await self.evt_resample_ir_chart.call(ir_arr)
        return [ resampled_ir.to_dict(orient='list'), time_stamp.tolist() ]
