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
            self.evt_load_data = manager.get_handler_module('LOAD_DATA_FROM_REDIS')
            self.evt_group_exists = manager.get_handler_module('MANIPULATE_REDIS').check_group_existence
        except Exception as e:
            import traceback
            traceback.print_exc()
        return handler_spec

    async def handle(self, event):     
        return {}

    async def call(self, recording_spl_rate: int, swept_sine_spl_rate: int):
        recording_df = await self.evt_load_data.load_group_data('convolution_recording')
        swept_sine_exist = await self.evt_group_exists('convolution_swept_sine', 'pkl')
        if (swept_sine_exist == False):
            anechoic_data = recording_df.values.T
            anechoic_data = anechoic_data / np.amax(anechoic_data)
        else:
            swept_sine_df = await self.evt_load_data.load_group_data('convolution_swept_sine')
            np_inv_swept_sine, inv_spl_rate = np.array(sf.read('./swept_sines/inv_swept_sine.wav'))
            #np_swept_sine = np.array(swept_sine)
            np_swept_sine = swept_sine_df.values.T
            room_ir = np.convolve(np_swept_sine, np_inv_swept_sine)
            room_ir = room_ir/np.amax(room_ir)
            offset_ind = np.where(np.abs(room_ir) > 0.1)[0][0]
            room_ir = room_ir[offset_ind - 4410:]
            ret[ret < 0.001] = 0

            np_recording = recording_df.values.T

            fft_len = 1
            while 2*fft_len < len(room_ir) + len(np_recording) - 1:
                fft_len *= 2
            fft_len *= 2

            room_ir_fft = np.fft.fft(room_ir, n=fft_len)
            recording_fft = np.fft.fft(np_recording, n=fft_len)
            anechoic_fft = recording_fft / room_ir_fft

            anechoic_data = np.fft.ifft(cv_sound_fft)
            anechoic_data = anechoic_data.real
            anechoic_data = anechoic_data / np.amax(anechoic_data)
        return [anechoic_data, recording_spl_rate]
