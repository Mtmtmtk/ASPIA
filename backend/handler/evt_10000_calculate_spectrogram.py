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
        return handler_spec

    async def handle(self, event):     
        return await {}

    async def call(self,test_message:str):
        return {}

    async def preprocess(self,sampling_points):
        sample_audio, sample_sr = sf.read('./impulse_response/Stairway/stereo/stairwell_ortf.wav')
        mono_audio = []
        if(isinstance(sample_audio[0], np.ndarray) == False):
            mono_audio = sample_audio
        elif(len(sample_audio[0]) == 2):
            mono_audio = (sample_audio[:,0] + sample_audio[:,1]) / 2
        elif(len(sample_audio[0]) == 4):
            mono_audio = sample_audio[:,0]
        mono_audio = resampy.resample(mono_audio,sample_sr,44100)
        N = sampling_points
        overlap = N / 2
        window = np.hamming(N)
        audio_length = len(mono_audio)
        overlap_trials = math.floor(audio_length / overlap) - 1
        first_center_freq = sample_sr/N/2
        last_center_freq = sample_sr/2
        freq_bin = np.round(np.arange(first_center_freq, last_center_freq, sample_sr/N),3)
        return [mono_audio, 44100, N, overlap, window, overlap_trials, freq_bin]

    async def get_amplitude(self, sampling_points:int):
        [mono_audio, sample_sr, N, overlap, window, overlap_trials, freq_bin] = await self.preprocess(sampling_points)
        df_fft = pd.DataFrame(index=range(int(N/2)*overlap_trials),columns=['time','center_frequency','amplitude']) 
        for i in range(overlap_trials):
            start = int((N-overlap) * i)
            end = int(start + N)
            windowed_frame = window * mono_audio[start:end]
            time  = round((start + end) / 2 / sample_sr,3)
            fft   = np.fft.fft(windowed_frame, n=N)
            fft_below_fs = fft[0:int(N/2)]
            amp   = np.abs(fft_below_fs)
            df_fft.loc[len(fft_below_fs)*i:len(fft_below_fs)*(i+1)-1,'time'] = time
            df_fft.loc[len(fft_below_fs)*i:len(fft_below_fs)*(i+1)-1,'center_frequency'] = freq_bin
            df_fft.loc[len(fft_below_fs)*i:len(fft_below_fs)*(i+1)-1,'amplitude'] = amp
        np_amp = df_fft['amplitude'].values
        np_amp = np_amp/np.amax(np_amp)
        df_fft.loc[:,'amplitude'] = np_amp
        print(df_fft)
        return df_fft

    async def get_power(self, sampling_points):
        [mono_audio, sample_sr, N, overlap, window, overlap_trials, freq_bin] = await self.preprocess(sampling_points)
        df_fft = pd.DataFrame(index=range(int(N/2)*overlap_trials),columns=['time','center_frequency','amplitude','power']) 
        for i in range(overlap_trials):
            start = int((N-overlap) * i)
            end = int(start + N)
            windowed_frame = window * mono_audio[start:end]
            time  = round((start + end) / 2 / sample_sr,3)
            fft   = np.fft.fft(windowed_frame, n=N)
            fft_below_fs = fft[0:int(N/2)]
            amp   = np.abs(fft_below_fs)
            power = amp ** 2
            df_fft.loc[len(fft_below_fs)*i:len(fft_below_fs)*(i+1)-1,'time'] = time
            df_fft.loc[len(fft_below_fs)*i:len(fft_below_fs)*(i+1)-1,'center_frequency'] = freq_bin
            df_fft.loc[len(fft_below_fs)*i:len(fft_below_fs)*(i+1)-1,'amplitude'] = amp
        np_amp = df_fft['amplitude'].values
        np_decibel = (np_amp ** 2)/np.amax(np_amp**2)
        df_fft.loc[:,'power']=np_decibel
        df_fft.drop(columns='amplitude')
        print(df_fft)
        return df_fft

    async def get_decibel(self, sampling_points):
        [mono_audio, sample_sr, N, overlap, window, overlap_trials, freq_bin] = await self.preprocess(sampling_points)
        df_fft = pd.DataFrame(index=range(int(N/2)*overlap_trials),columns=['time','center_frequency','power','decibel']) 
        for i in range(overlap_trials):
            start = int((N-overlap) * i)
            end = int(start + N)
            windowed_frame = window * mono_audio[start:end]
            time  = round((start + end) / 2 / sample_sr,3)
            fft   = np.fft.fft(windowed_frame, n=N)
            fft_below_fs = fft[0:int(N/2)]
            amp   = np.abs(fft_below_fs)
            power = amp ** 2
            df_fft.loc[len(fft_below_fs)*i:len(fft_below_fs)*(i+1)-1,'time'] = time
            df_fft.loc[len(fft_below_fs)*i:len(fft_below_fs)*(i+1)-1,'center_frequency'] = freq_bin
            df_fft.loc[len(fft_below_fs)*i:len(fft_below_fs)*(i+1)-1,'power'] = power
        np_power = df_fft['power'].values
        np_decibel = np.log10((np_power/np.amax(np_power)).astype(np.float64))
        df_fft.loc[:,'decibel'] = np_decibel
        df_fft.drop(columns='power')
        return df_fft
