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
        self.evt_reshape_ir = manager.get_handler_module('RESHAPE_IR')
        return handler_spec

    async def handle(self, event):     
        return await self.call(**event.data)

    async def call(self, ir_arr, spl_rate: int, channels:int):
        reshaped_ir = await self.evt_reshape_ir.call(ir_arr, spl_rate, channels)
        reshaped_ir = reshaped_ir[reshaped_ir.index % 10 == 0]
        return reshaped_ir.to_dict(orient='list')
