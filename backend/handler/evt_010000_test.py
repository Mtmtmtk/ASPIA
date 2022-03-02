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
        return await self.call(**event.data)

    async def call(self, test_running:str):
        print(test_running)
        np_inv_swept_sine, inv_spl_rate = np.array(sf.read('./swept_sines/inv_swept_sine.wav'))
        #np_swept_sine, spl_rate = np.array(sf.read('./swept_sines/swept_sine.wav'))
        np_owariya, spl_rate = np.array(sf.read('./owariya.wav'))
        np_recorder, recorder_spl_rate = np.array(sf.read('./recorder.wav'))
        #fft_len = 1
        #while 2*fft_len < len(np_owariya) - 1:
        #    fft_len *= 2
        #fft_len *= 2

        ret = np.convolve(np_owariya, np_inv_swept_sine)
        ret = ret/np.amax(ret)
        offset_ind = np.where(np.abs(ret) > 0.1)[0][0]
        ret = ret[offset_ind - 4410:]
        ret[ret < 0.001] = 0

        write('owariya_convolve.wav', spl_rate, ret)

        fft_len = 1
        while 2*fft_len < len(ret) + len(np_recorder) - 1:
            fft_len *= 2
        fft_len *= 2

        ret_fft = np.fft.fft(ret, n=fft_len)
        recorder_fft = np.fft.fft(np_recorder, n=fft_len)
        cv_sound_fft = recorder_fft / ret_fft

        cv_sound = np.fft.ifft(cv_sound_fft)
        cv_sound = cv_sound.real
        cv_sound = cv_sound / np.amax(cv_sound)
        write('recorder_anechoic.wav', spl_rate, cv_sound)

        return {}
