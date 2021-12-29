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

    async def call(self, recording, sampling_rate: int, path:str):
        anechoic_data = np.array(recording)
        anechoic_data = anechoic_data / np.amax(anechoic_data)
        anechoic_data = np.where(anechoic_data < 0.0001,0,anechoic_data);

        anechoic_sr = sampling_rate
        ir_data, ir_sr = sf.read(path)

        return [anechoic_data, anechoic_sr, ir_data, ir_sr]
