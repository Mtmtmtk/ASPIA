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
        try:
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
        return await self.call(**event.data)

    async def call(self, ir_arr, spl_rate: int, channels:int, filter_type:str, order:int):
        average_ir = await self.evt_pick_representative_ir.call(ir_arr,channels)

        df_parameter = pd.DataFrame(0, columns=['31.5','63','125','250','500','1k','2k','4k','8k','16k'], index=['T30(RT60)','EDT','D50','C50','C80'])
        for octave in self.octave_band:
            fbp = octave['bandpass']
            filtered_signal = self.bandpassFilter(average_ir, spl_rate, fbp, filter_type, order)
            sr_filtered_signal = pd.Series(filtered_signal)
            print({'octave':octave['center']})
            print(sr_filtered_signal)
            df = pd.DataFrame(columns=['energy','sum_energy','schroeder','time_stamp'])
            df['energy'] = sr_filtered_signal**2
            total_energy = np.sum(df['energy'])
            energy_cumsum = np.cumsum(df['energy'])
            energy_cumsum = np.append(0, energy_cumsum)
            energy_cumsum = np.delete(energy_cumsum, -1)

            D_fifty  = round(np.sum(df['energy'][:int(0.05*spl_rate)])/total_energy, 2)
            C_fifty  = round(10 * np.log10(np.sum(df['energy'][:int(0.05*spl_rate)])/np.sum(df['energy'][int(0.05*spl_rate):])), 2)
            C_eighty = round(10 * np.log10(np.sum(df['energy'][:int(0.08*spl_rate)])/np.sum(df['energy'][int(0.08*spl_rate):])), 2)
            df_parameter.loc['D50',octave['center']] = D_fifty
            df_parameter.loc['C50',octave['center']] = C_fifty
            df_parameter.loc['C80',octave['center']] = C_eighty

            df['sum_energy'] = total_energy - energy_cumsum
            df['schroeder'] = 10 * np.log10(df['sum_energy']/total_energy)
            df['time_stamp'] = df.index * 1/spl_rate
            df = df.drop(columns=['energy','sum_energy'])

            minus_five_db = {}
            minus_five_db['time_stamp'] = (df.query('schroeder >= -5')[::-1].iloc[0]['time_stamp'] + df.query('schroeder <= -5').iloc[0]['time_stamp'])/2
            minus_five_db['schroeder'] = (df.query('schroeder >= -5')[::-1].iloc[0]['schroeder'] + df.query('schroeder <= -5').iloc[0]['schroeder'])/2
            minus_ten_db = {}
            minus_ten_db['time_stamp'] = (df.query('schroeder >= -10')[::-1].iloc[0]['time_stamp'] + df.query('schroeder <= -10').iloc[0]['time_stamp'])/2
            minus_ten_db['schroeder'] = (df.query('schroeder >= -10')[::-1].iloc[0]['schroeder'] + df.query('schroeder <= -10').iloc[0]['schroeder'])/2
            minus_thirtyfive_db = {}
            minus_thirtyfive_db['time_stamp'] = (df.query('schroeder >= -35')[::-1].iloc[0]['time_stamp'] + df.query('schroeder <= -35').iloc[0]['time_stamp'])/2
            minus_thirtyfive_db['schroeder'] = (df.query('schroeder >= -35')[::-1].iloc[0]['schroeder'] + df.query('schroeder <= -35').iloc[0]['schroeder'])/2

            df_parameter.loc['T30(RT60)', octave['center']] = round(11/6*minus_thirtyfive_db['time_stamp']-5/6*minus_five_db['time_stamp'],2)
            df_parameter.loc['EDT', octave['center']] = round(6*minus_ten_db['time_stamp'],2)

        df_parameter = df_parameter.reset_index()
        df_parameter = df_parameter.rename(columns={'index':'parameter'})
        return df_parameter.to_dict('records')

    def bandpassFilter(self, ir, fs, fbp, filter_type, order):
        nyq = fs / 2.0 
        normalized_cutoff = np.array(fbp) / nyq
        b=[]
        a=[]
        if filter_type=='Butterworth':
            b,a = signal.butter(order, normalized_cutoff, btype='band', analog=False)
        elif filter_type=='Chebychev1':
            b,a = signal.cheby1(order, rp=5, Wn=normalized_cutoff, btype='band', analog=False)
        elif filter_type=='Chebychev2':
            b,a = signal.cheby2(order, rs=5, Wn=normalized_cutoff, btype='band', analog=False)
        elif filter_type=='Elliptic':
            b,a = signal.ellip(order, rp=5, rs=5, Wn=normalized_cutoff, btype='band', analog=False)
        elif filter_type=='Bessel':
            b,a = signal.bessel(order, Wn=normalized_cutoff, btype='band', analog=False)
        elif filter_type=='FIR':
            b = signal.firwin(numtaps=order, cutoff=np.array(fbp), fs=fs, pass_zero=False)
            a = 1
        filtered_ir = signal.lfilter(b,a,ir)
        return filtered_ir