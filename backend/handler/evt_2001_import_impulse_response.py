from ducts.spi import EventHandler
import numpy as np
import pandas as pd
from scipy.io.wavfile import write
import soundfile as sf
import resampy
from scheme.status import ForecastStatus

import logging
logger = logging.getLogger(__name__)

class Handler(EventHandler):

    def __init__(self):
        super().__init__()

    def setup(self, handler_spec, manager):
        handler_spec.set_description('UK Dissertation')
        try:
            self.evt_status = manager.get_handler_module('STATUS')
        except Exception as e:
            import traceback
            traceback.print_exc()
        return handler_spec

    async def handle(self, event):     
        return {}

    async def call(self, path:str):
        await self.evt_status.set(ForecastStatus.IMPORT_IR)
        ir_data, ir_sr = sf.read(path)
        return [ir_data, ir_sr]
