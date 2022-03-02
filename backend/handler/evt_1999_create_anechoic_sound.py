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

    async def call(self, recording, recording_spl_rate: int, swept_sine, swept_sine_spl_rate: int):
        anechoic_data = []
        if swept_sine == [] or swept_sine_spl_rate == 0:
            anechoic_data = np.array(recording)
            anechoic_data = anechoic_data / np.amax(anechoic_data)
        else:
            np_inv_swept_sine, inv_spl_rate = np.array(sf.read('./swept_sines/inv_swept_sine.wav'))
            np_swept_sine = np.array(swept_sine)
            room_ir = np.convolve(np_swept_sine, np_inv_swept_sine)
            room_ir = room_ir/np.amax(room_ir)
            offset_ind = np.where(np.abs(room_ir) > 0.1)[0][0]
            room_ir = room_ir[offset_ind - 4410:]
            ret[ret < 0.001] = 0

            np_recording = np.array(recording)

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
