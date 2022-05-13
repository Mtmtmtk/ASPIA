from ducts.spi import EventHandler
import numpy as np
import pandas as pd
from scipy.io.wavfile import write
import soundfile as sf
import resampy
import math

import logging
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

    async def call(self,test_message:str):
        return {}

    async def get_window(self, window_type: str, sampling_points: int):
        window = []
        N = sampling_points
        if window_type == 'Hamming':
            window = np.hamming(N)
        elif window_type == 'Hann':
            window = np.hanning(N)
        elif window_type == 'Blackman':
            window = np.blackman(N)
        return window


