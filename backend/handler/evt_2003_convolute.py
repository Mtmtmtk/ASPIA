from ducts.spi import EventHandler
import numpy as np
import pandas as pd
from scipy.io.wavfile import write
import soundfile as sf
from scheme.status import ForecastStatus
import resampy

import logging
logger = logging.getLogger(__name__)

class Handler(EventHandler):

    def __init__(self):
        super().__init__()

    def setup(self, handler_spec, manager):
        try:
            self.evt_resample = manager.get_handler_module('RESAMPLE')
            self.evt_status = manager.get_handler_module('STATUS')
        except Exception as e:
            import traceback
            traceback.print_exc()
        return handler_spec

    async def handle(self, event):     
        return {}

    async def call(self, recording_spl_rate: int, swept_sine_spl_rate:int, ir_path:str, output_channels: str):
        [anechoic_data, ir_resampled, fft_len] = await self.evt_resample.call(recording_spl_rate, swept_sine_spl_rate, ir_path, output_channels)
        await self.evt_status.set(ForecastStatus.START_CONVOLUTION)
        ir_resampled_fft = np.fft.fft(ir_resampled, n=fft_len)
        anechoic_fft = np.fft.fft(anechoic_data, n=fft_len)
        cv_sound_fft = ir_resampled_fft * anechoic_fft

        cv_sound = np.fft.ifft(cv_sound_fft)
        cv_sound = cv_sound.real
        cv_sound = cv_sound / np.amax(cv_sound)
        cv_sound = cv_sound.tolist()
        await self.evt_status.set(ForecastStatus.CONVOLUTION_FINISHED)
        return cv_sound
