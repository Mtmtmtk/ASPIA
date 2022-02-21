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
        try:
            self.evt_resample = manager.get_handler_module('RESAMPLE')
        except Exception as e:
            import traceback
            traceback.print_exc()
        return handler_spec

    async def handle(self, event):     
        return {}

    async def call(self, recording, sampling_rate: int, path:str, output_channels: str):
        [anechoic_data, ir_resampled, fft_len,sr] = await self.evt_resample.call(recording,sampling_rate, path, output_channels)

        ir_resampled_fft = np.fft.fft(ir_resampled, n=fft_len)
        anechoic_fft = np.fft.fft(anechoic_data, n=fft_len)
        cv_sound_fft = ir_resampled_fft * anechoic_fft

        cv_sound = np.fft.ifft(cv_sound_fft)
        cv_sound = cv_sound.real
        cv_sound = cv_sound / np.amax(cv_sound)
        cv_sound = cv_sound.tolist()
        return cv_sound
