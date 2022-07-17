from ducts.spi import EventHandler
import numpy as np
import pandas as pd
from scipy import signal
import logging
import resampy
logger = logging.getLogger(__name__)

class Handler(EventHandler):

    def __init__(self):
        super().__init__()

    def setup(self, handler_spec, manager):
        handler_spec.set_description('UK Dissertation')
        try:
            self.evt_load_data = manager.get_handler_module('LOAD_DATA_FROM_REDIS')
            self.evt_pick_representative_ir = manager.get_handler_module('PICK_REPRESENTATIVE_IR')
        except Exception as e:
            import traceback
            traceback.print_exc()
        self.octave_band = [
            { 'center': '31.5', 'bandpass':[22   ,44] },
            { 'center': '63'  , 'bandpass':[44   ,88] },
            { 'center': '125' , 'bandpass':[88   ,177] },
            { 'center': '250' , 'bandpass':[177  ,355] },
            { 'center': '500' , 'bandpass':[355  ,710] },
            { 'center': '1k'  , 'bandpass':[710  ,1420] },
            { 'center': '2k'  , 'bandpass':[1420 ,2840] },
            { 'center': '4k'  , 'bandpass':[2840 ,5680] },
            { 'center': '8k'  , 'bandpass':[5680 ,11360] },
            { 'center': '16k' , 'bandpass':[11360,22049] },
        ]
        return handler_spec

    async def handle(self, event):     
        return {}

    async def call(self, spl_rate: int, filter_type: str, order: int):
        return {}

    async def filter_signal(self, group_key: str, spl_rate: int, filter_type: str, order: int, ripple: int, attenuation: int):
        df_ir = await self.evt_load_data.load_group_data(group_key)
        list_ir = []
        for channel in df_ir.columns:
            list_ir.append(df_ir[channel].to_numpy())
        signal_dict = {}
        for octave in self.octave_band:
            df_filtered_signal = pd.DataFrame(columns=range(len(df_ir.columns)))
            fbp = octave['bandpass']
            filtered_signal = self.bandpassFilter(list_ir, spl_rate, fbp, filter_type, order, ripple, attenuation)
            filtered_signal_resampled = resampy.resample(filtered_signal, 44100, 44100/10)
            signal_dict[octave['center']] = pd.DataFrame(filtered_signal_resampled).T
        return signal_dict

    def bandpassFilter(self, ir, fs, fbp, filter_type, order, ripple, attenuation):
        nyq = fs / 2.0 
        normalized_cutoff = np.array(fbp) / nyq
        b=[]
        a=[]
        if filter_type=='Butterworth':
            b,a = signal.butter(order, normalized_cutoff, btype='band', analog=False)
        elif filter_type=='Chebychev1':
            b,a = signal.cheby1(order, rp=ripple, Wn=normalized_cutoff, btype='band', analog=False)
        elif filter_type=='Chebychev2':
            b,a = signal.cheby2(order, rs=attenuation, Wn=normalized_cutoff, btype='band', analog=False)
        elif filter_type=='Elliptic':
            b,a = signal.ellip(order, rp=ripple, rs=attenuation, Wn=normalized_cutoff, btype='band', analog=False)
        elif filter_type=='Bessel':
            b,a = signal.bessel(order, Wn=normalized_cutoff, btype='band', analog=False)
        elif filter_type=='FIR':
            b = signal.firwin(numtaps=order, cutoff=np.array(fbp), fs=fs, pass_zero=False)
            a = 1
        filtered_ir = signal.lfilter(b,a,ir)
        return filtered_ir
