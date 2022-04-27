from ducts.spi import EventHandler
import io
import pickle
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
            self.evt_spectrogram = manager.get_handler_module('CALCULATE_SPECTROGRAM')
        except Exception as e:
            import traceback
            traceback.print_exc()
        return handler_spec

    async def handle(self, event):     
        return await self.call(**event.data)

    async def call(self, spl_rate:int, sampling_points:int):
        df =  await self.evt_spectrogram.get_decibel(spl_rate, sampling_points)
        z_data = df.groupby('center_frequency')['decibel'].apply(list).tolist()
        freq_bin = df['center_frequency'].drop_duplicates().tolist()
        timestamp = df['time'].drop_duplicates().tolist()
        return [ freq_bin, z_data, timestamp ]
