from ducts.spi import EventHandler
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
        handler_spec.set_description('UK Dissertation')
        return handler_spec

    async def handle(self, event):     
        return {}

    async def call(self, path:str):
        ir_data, ir_sr = sf.read(path)
        return [ir_data, ir_sr]
