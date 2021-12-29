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
            self.evt_import_files = manager.get_handler_module('IMPORT_SOUND_FILES')
        except Exception as e:
            import traceback
            traceback.print_exc()
        return handler_spec

    async def handle(self, event):     
        return {}

    async def call(self, recording, sampling_rate: int, path:str, output_channels: str):
        [anechoic_data, anechoic_sr, ir_data, ir_sr] = await self.evt_import_files.call(recording, sampling_rate, path)

        cv_sound_fft = []
        cv_sound = []

        output_ir = []
        fft_len = 1

        if output_channels == 'mono':
            ir = []
            if len(ir_data[0]) == 1:
                ir = ir_data[:,0]
            else:
                ir_left = []
                ir_right = []
                if len(ir_data[0]) == 2:
                    ir_left = ir_data[:,0]
                    ir_right = ir_data[:,1]
                elif len(ir_data[0]) == 4:
                    ir_left = ir_data[:,0] + 0.707*ir_data[:,2]
                    ir_right = ir_data[:,0] - 0.707*ir_data[:,2]
                ir = (ir_left + ir_right) / 2

            ir_resampled = resampy.resample(ir, ir_sr, anechoic_sr)

            output_ir = ir_resampled / np.amax(ir_resampled)
        elif output_channels == 'stereo':
            ir_left = []
            ir_right = []
            if len(ir_data[0]) ==2:
                ir_left = ir_data[:,0]
                ir_right = ir_data[:,1]
            elif len(ir_data[0]) == 4:
                ir_left = ir_data[:,0] + 0.707*ir_data[:,2]
                ir_right = ir_data[:,0] - 0.707*ir_data[:,2]
            
            ir_left_resampled = resampy.resample(ir_left, ir_sr, anechoic_sr)
            ir_right_resampled = resampy.resample(ir_right, ir_sr, anechoic_sr)

            output_ir = np.array([ir_left_resampled, ir_right_resampled])
            output_ir = output_ir / np.amax(output_ir)
        elif output_channels == 'b-format':
            ir_W = ir_data[:,0]
            ir_Y = ir_data[:,1]
            ir_Z = ir_data[:,2]
            ir_X = ir_data[:,3]
            
            ir_W_resampled = resampy.resample(ir_W, ir_sr, anechoic_sr)
            ir_Y_resampled = resampy.resample(ir_Y, ir_sr, anechoic_sr)
            ir_Z_resampled = resampy.resample(ir_Z, ir_sr, anechoic_sr)
            ir_X_resampled = resampy.resample(ir_X, ir_sr, anechoic_sr)

            output_ir = np.array([ir_W_resampled, ir_Y_resampled, ir_Z_resampled, ir_X_resampled])
            output_ir = output_ir / np.amax(output_ir)

        while 2*fft_len < len(output_ir[0]) + len(anechoic_data) - 1:
            fft_len *= 2
        fft_len *= 2

        return [anechoic_data ,output_ir, fft_len]


