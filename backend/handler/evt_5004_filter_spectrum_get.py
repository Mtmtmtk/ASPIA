from ducts.spi import EventHandler
import numpy as np
import pandas as pd
from scipy import signal
import logging
logger = logging.getLogger(__name__)

class Handler(EventHandler):

    def __init__(self):
        super().__init__()

    def setup(self, handler_spec, manager):
        handler_spec.set_description('UK Dissertation')
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
        return await self.call(**event.data)

    async def call(self, spl_rate:int, filter_type:str, order:int):
        df_amp = pd.DataFrame(columns = ['31.5','63','125','250','500','1k','2k','4k','8k','16k'])
        sr_freq = []
        isStableDict = {}
        stabilityCheckList = []
        for octave in self.octave_band:
            fbp = octave['bandpass']
            [ amp_dB, w, isStable ] = self.bandpassFreqResponse(spl_rate, fbp, filter_type, order)
            df_amp[octave['center']] = amp_dB
            sr_freq = pd.Series(w)
            stabilityCheckList.append({ 'hz': octave['center'], 'isStable': isStable })
        return [ df_amp.to_dict(orient='list'), sr_freq.tolist(), stabilityCheckList ]

    def bandpassFreqResponse(self, fs, fbp, filter_type, order):
        iir_filters = ['Butterworth','Chebychev1','Chebychev2','Elliptic','Bessel']
        nyq = fs / 2.0 
        normalized_cutoff = np.array(fbp) / nyq
        b = []
        a = []
        if filter_type=='Butterworth':
            b,a = signal.butter(order, normalized_cutoff, btype='band', analog=False)
        elif filter_type=='Chebychev1':
            b,a = signal.cheby1(order, rp = 5, Wn=normalized_cutoff, btype='band', analog=False)
        elif filter_type=='Chebychev2':
            b,a = signal.cheby2(order, rs = 5, Wn=normalized_cutoff, btype='band', analog=False)
        elif filter_type=='Elliptic':
            b,a = signal.ellip(order, rp = 5, rs = 5, Wn=normalized_cutoff, btype='band', analog=False)
        elif filter_type=='Bessel':
            b,a = signal.bessel(order, Wn=normalized_cutoff, btype='band', analog=False)
        elif filter_type=='FIR':
            print(order)
            print(fbp)
            b = signal.firwin(numtaps=order, cutoff=np.array(fbp), fs=fs, pass_zero=False)
            a = 1
        w,h = signal.freqz(b,a, worN = 2048 ,fs=fs)
        isStable = True
        if filter_type in iir_filters:
            if True in (np.abs(np.roots(a)) > 1):
                isStable = False
        amp_dB = 20 * np.log10(np.abs(h)/np.max(np.abs(h)))
        return [ amp_dB, w, isStable ]
