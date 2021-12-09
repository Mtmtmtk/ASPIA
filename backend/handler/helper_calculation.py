import numpy as np
import pandas as pd
from scipy.io.wavfile import write
import soundfile as sf
import resampy

class Convolution():    
    def __init__(self):
        super().__init__()

    async def convolute(self, recording, ir):
        anechoic_data = recording
        anechoic_sr = 48000
        ir_data, ir_sr = sf.read('1st_baptist_nashville_balcony.wav')
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
        stereo_ir = np.array([ir_left_resampled, ir_right_resampled])
        stereo_ir = stereo_ir / np.amax(stereo_ir)
        stereo_ir_fft = np.fft.fft(stereo_ir, n=len(anechoic_data))
        anechoic_fft = np.fft.fft(anechoic_data, n=len(anechoic_data))
        cv_sound_fft = stereo_ir_fft * anechoic_fft
        cv_sound = np.fft.ifft(cv_sound_fft)
        cv_sound = cv_sound.real
        #cv_sound = [np.convolve(anechoic_data, stereo_ir[0]), np.convolve(anechoic_data, stereo_ir[1])]
        cv_sound = cv_sound / np.amax(cv_sound)

        print('hoge')
        cv_sound = cv_sound.T

        write('convoluted.wav', anechoic_sr, cv_sound)
        cv_sound = cv_sound.T.tolist()
        print(cv_sound)
        return cv_sound

