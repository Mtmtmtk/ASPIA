import numpy as np
import pandas as pd
from scipy.io.wavfile import write
import soundfile as sf
import resampy

class Convolution():    
    def __init__(self):
        super().__init__()

    async def convolute(self, recording, sampling_rate, path, output_channels):
        anechoic_data = np.array(recording)
        anechoic_data = anechoic_data / np.amax(anechoic_data)
        anechoic_data = np.where(anechoic_data < 0.0001,0,anechoic_data);

        anechoic_sr = sampling_rate
        ir_data, ir_sr = sf.read(path)
        cv_sound_fft = []
        cv_sound = []

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

            fft_len = 1
            while 2*fft_len < len(ir_resampled) + len(anechoic_data) - 1:
                fft_len *= 2
            fft_len *= 2

            mono_ir = ir_resampled / np.amax(ir_resampled)
            mono_ir_fft = np.fft.fft(mono_ir, n=fft_len)
            anechoic_fft = np.fft.fft(anechoic_data, n=fft_len)
            cv_sound_fft = mono_ir_fft * anechoic_fft
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

            fft_len = 1
            while 2*fft_len < len(ir_left_resampled) + len(anechoic_data) - 1:
                fft_len *= 2
            fft_len *= 2

            stereo_ir = np.array([ir_left_resampled, ir_right_resampled])
            stereo_ir = stereo_ir / np.amax(stereo_ir)
            stereo_ir_fft = np.fft.fft(stereo_ir, n=fft_len)
            anechoic_fft = np.fft.fft(anechoic_data, n=fft_len)
            cv_sound_fft = stereo_ir_fft * anechoic_fft
        elif output_channels == 'b-format':
            ir_W = ir_data[:,0]
            ir_Y = ir_data[:,1]
            ir_Z = ir_data[:,2]
            ir_X = ir_data[:,3]
            
            ir_W_resampled = resampy.resample(ir_W, ir_sr, anechoic_sr)
            ir_Y_resampled = resampy.resample(ir_Y, ir_sr, anechoic_sr)
            ir_Z_resampled = resampy.resample(ir_Z, ir_sr, anechoic_sr)
            ir_X_resampled = resampy.resample(ir_X, ir_sr, anechoic_sr)

            fft_len = 1
            while 2*fft_len < len(ir_W_resampled) + len(anechoic_data) - 1:
                fft_len *= 2
            fft_len *= 2

            b_format_ir = np.array([ir_W_resampled, ir_Y_resampled, ir_Z_resampled, ir_X_resampled])
            b_format_ir = b_format_ir / np.amax(b_format_ir)
            b_format_ir_fft = np.fft.fft(b_format_ir, n=fft_len)
            anechoic_fft = np.fft.fft(anechoic_data, n=fft_len)
            cv_sound_fft = b_format_ir_fft * anechoic_fft




        cv_sound = np.fft.ifft(cv_sound_fft)
        cv_sound = cv_sound.real
        cv_sound = cv_sound / np.amax(cv_sound)
        cv_sound = cv_sound.tolist()
        return cv_sound
