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
        try:
            self.evt_load_data = manager.get_handler_module('LOAD_DATA_FROM_REDIS')
        except Exception as e:
            import traceback
            traceback.print_exc()
        return handler_spec

    async def handle(self, event):     
        return {}

    async def call(self,test_message:str):
        return {}

    async def preprocess(self, spl_rate:int, sampling_points:int, window_type: str, overlap_per: int):
        df = await self.evt_load_data.load_group_data('spectrogram')
        sample_sr = spl_rate
        mono_audio = []
        channels = len(df.columns)
        if (channels == 4) or (channels == 1):
            mono_audio = df.iloc[:,0]
        elif channels == 2:
            mono_audio = df.mean(axis='columns')
        mono_audio = np.array(mono_audio.tolist())
        mono_audio = resampy.resample(mono_audio,sample_sr,44100)
        N = sampling_points
        overlap = N / 100 * overlap_per
        audio_length = len(mono_audio)
        overlap_trials = math.floor(audio_length / (N - overlap))
        zero_padding = np.zeros(int(((audio_length / (N - overlap)) + 1)*(N - overlap) - audio_length))
        mono_audio = np.concatenate((mono_audio, zero_padding))
        window = []
        if window_type == 'Hamming':
            window = np.hamming(N)
        elif window_type == 'Hann':
            window = np.hanning(N)
        elif window_type == 'Blackman':
            window = np.blackman(N)
        else:
            window = np. hamming(N)
        first_center_freq = 0
        last_center_freq = sample_sr/2
        freq_bin = np.round(np.arange(first_center_freq, last_center_freq, sample_sr/N),3)
        return [mono_audio, 44100, N, overlap, window, overlap_trials, freq_bin]

    async def get_amplitude(self, spl_rate:int, sampling_points:int, window_type: str, overlap_per: int):
        [mono_audio, sample_sr, N, overlap, window, overlap_trials, freq_bin] = await self.preprocess(spl_rate, sampling_points, window_type, overlap_per)
        df_fft = pd.DataFrame(index=range(int(N/2)*overlap_trials),columns=['time','center_frequency','amplitude']) 

        np_time = df_fft.loc[:, 'time'].values
        np_center_freq = df_fft.loc[:, 'center_frequency'].values
        np_amp = df_fft.loc[:, 'amplitude'].values

        sr_trials = pd.Series(range(overlap_trials))
        sr_trials.apply(self.execute_fft, args=(np_time, np_center_freq, np_amp, mono_audio, window, sample_sr, N, overlap, freq_bin, ))

        df_fft['time'] = np_time
        df_fft['center_frequency'] = np_center_freq
        df_fft['amplitude'] = np_amp

        df_fft = df_fft[df_fft['time'].notna()]

        np_amp = df_fft['amplitude'].values
        np_amp = np_amp/np.amax(np_amp)
        df_fft['amplitude'] = np_amp
        return df_fft

    async def get_power(self, spl_rate:int, sampling_points:int, window_type: str, overlap_per: int):
        [mono_audio, sample_sr, N, overlap, window, overlap_trials, freq_bin] = await self.preprocess(spl_rate, sampling_points, window_type, overlap_per)
        df_fft = pd.DataFrame(index=range(int(N/2)*overlap_trials),columns=['time','center_frequency','amplitude','power']) 

        np_time = df_fft.loc[:, 'time'].values
        np_center_freq = df_fft.loc[:, 'center_frequency'].values
        np_amp = df_fft.loc[:, 'amplitude'].values

        sr_trials = pd.Series(range(overlap_trials))
        sr_trials.apply(self.execute_fft, args=(np_time, np_center_freq, np_amp, mono_audio, window, sample_sr, N, overlap, freq_bin, ))

        df_fft['time'] = np_time
        df_fft['center_frequency'] = np_center_freq
        df_fft['amplitude'] = np_amp

        df_fft = df_fft[df_fft['time'].notna()]

        np_amp = df_fft['amplitude'].values
        np_power = (np_amp ** 2)/np.amax(np_amp**2)
        df_fft.loc[:,'power'] = np_power
        df_fft.drop(columns='amplitude')
        return df_fft

    async def get_decibel(self, spl_rate:int, sampling_points:int, window_type: str, overlap_per: int):
        [mono_audio, sample_sr, N, overlap, window, overlap_trials, freq_bin] = await self.preprocess(spl_rate, sampling_points, window_type, overlap_per)
        df_fft = pd.DataFrame(index=range(int(N/2)*overlap_trials),columns=['time','center_frequency', 'amplitude', 'power', 'decibel']) 

        np_time = df_fft.loc[:, 'time'].values
        np_center_freq = df_fft.loc[:, 'center_frequency'].values
        np_amp = df_fft.loc[:, 'amplitude'].values

        sr_trials = pd.Series(range(overlap_trials))
        sr_trials.apply(self.execute_fft, args=(np_time, np_center_freq, np_amp, mono_audio, window, sample_sr, N, overlap, freq_bin, ))

        df_fft['time'] = np_time
        df_fft['center_frequency'] = np_center_freq
        df_fft['amplitude'] = np_amp

        df_fft = df_fft[df_fft['time'].notna()]
        np_amp = df_fft['amplitude'].values
        np_amp = np_amp/np.amax(np_amp)
        df_fft.loc[:,'amplitude'] = np_amp
        np_power = np_amp ** 2
        df_fft.loc[:,'power'] = np_power
        np_decibel = np.log10((np_power/np.amax(np_power)).astype(np.float64))
        df_fft.loc[:,'decibel'] = np_decibel
        df_fft.drop(columns='power')
        return df_fft
    
    async def get_all(self, spl_rate: int, sampling_points: int, window_type: str, overlap_per: int):
        [mono_audio, sample_sr, N, overlap, window, overlap_trials, freq_bin] = await self.preprocess(spl_rate, sampling_points, window_type, overlap_per)
        df_fft = pd.DataFrame(index=range(int(N/2)*overlap_trials),columns=['time','center_frequency', 'amplitude', 'power', 'decibel']) 

        np_time = df_fft.loc[:, 'time'].values
        np_center_freq = df_fft.loc[:, 'center_frequency'].values
        np_amp = df_fft.loc[:, 'amplitude'].values

        sr_trials = pd.Series(range(overlap_trials))
        sr_trials.apply(self.execute_fft, args=(np_time, np_center_freq, np_amp, mono_audio, window, sample_sr, N, overlap, freq_bin, ))

        df_fft['time'] = np_time
        df_fft['center_frequency'] = np_center_freq
        df_fft['amplitude'] = np_amp

        df_fft = df_fft[df_fft['time'].notna()]
        np_amp = df_fft['amplitude'].values
        np_amp = np_amp/np.amax(np_amp)
        df_fft.loc[:,'amplitude'] = np_amp
        np_power = np_amp ** 2
        df_fft.loc[:,'power'] = np_power
        np_decibel = np.log10((np_power/np.amax(np_power)).astype(np.float64))
        df_fft.loc[:,'decibel'] = np_decibel
        return df_fft


    def execute_fft(self, frame_idx, np_time, np_center_freq, np_amp, mono_audio, window, sample_sr, N, overlap, freq_bin):
        start = int((N-overlap) * frame_idx)
        end = int(start + N)
        frame_len = len(mono_audio[start:end])
        if(frame_len == N):
            windowed_frame = window * mono_audio[start:end]
            time  = round((start + end) / 2 / sample_sr,3)
            fft   = np.fft.fft(windowed_frame, n=N)
            fft_below_fs = fft[0:int(N/2)]
            amp   = np.abs(fft_below_fs)
            np_time[        len(fft_below_fs)*frame_idx : len(fft_below_fs)*(frame_idx+1)] = time
            np_center_freq[ len(fft_below_fs)*frame_idx : len(fft_below_fs)*(frame_idx+1)] = freq_bin
            np_amp[         len(fft_below_fs)*frame_idx : len(fft_below_fs)*(frame_idx+1)] = amp
