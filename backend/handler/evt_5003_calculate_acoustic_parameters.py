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
        return await self.call(**event.data)

    async def call(self, spl_rate: int, filter_type: str, order: int):
        return {}
    
    async def get_parameters(self, group_key: str, spl_rate: int, filter_type: str, order: int, ripple:int, attenuation:int):
        ir_df = await self.evt_load_data.load_group_data(group_key)
        average_ir = await self.evt_pick_representative_ir.call(ir_df)

        df_schroeder = pd.DataFrame(columns=['31.5','63','125','250','500','1k','2k','4k','8k','16k','time_stamp'])
        df_parameter = pd.DataFrame(0, columns=['31.5','63','125','250','500','1k','2k','4k','8k','16k'], index=['T30(RT60)','EDT','D50','C50','C80','Ts'])
        for octave in self.octave_band:
            fbp = octave['bandpass']
            filtered_signal = self.bandpassFilter(average_ir, spl_rate, fbp, filter_type, order, ripple, attenuation)
            sr_filtered_signal = pd.Series(filtered_signal)
            df = pd.DataFrame(columns=['energy','remaining_energy','schroeder','time_stamp'])
            df['energy'] = sr_filtered_signal**2
            df['time_stamp'] = df.index * 1/spl_rate
            total_energy = np.sum(df['energy'])
            energy_cumsum = np.cumsum(df['energy'])
            energy_cumsum = np.append(0, energy_cumsum)
            energy_cumsum = np.delete(energy_cumsum, -1)
            D_fifty  = round(np.sum(df['energy'][:int(0.05*spl_rate)])/total_energy, 2)
            C_fifty  = round(10 * np.log10(np.sum(df['energy'][:int(0.05*spl_rate)])/np.sum(df['energy'][int(0.05*spl_rate):])), 2)
            C_eighty = round(10 * np.log10(np.sum(df['energy'][:int(0.08*spl_rate)])/np.sum(df['energy'][int(0.08*spl_rate):])), 2)
            T_s      = round(np.sum(df['energy'] * df['time_stamp'])/total_energy, 2)
            df_parameter.loc['D50',octave['center']] = D_fifty
            df_parameter.loc['C50',octave['center']] = C_fifty
            df_parameter.loc['C80',octave['center']] = C_eighty
            df_parameter.loc['Ts' ,octave['center']] = T_s
            
            df['remaining_energy'] = total_energy - energy_cumsum
            df['schroeder'] = 10 * np.log10(df['remaining_energy']/total_energy)
            df = df.drop(columns=['energy','remaining_energy'])

            df_schroeder[octave['center']] = df['schroeder']

            minus_five_db = {}
            minus_five_db['time_stamp'] = (df.query('schroeder >= -5')[::-1].iloc[0]['time_stamp'] + df.query('schroeder <= -5').iloc[0]['time_stamp'])/2
            minus_five_db['schroeder']  = (df.query('schroeder >= -5')[::-1].iloc[0]['schroeder']  + df.query('schroeder <= -5').iloc[0]['schroeder'] )/2
            minus_ten_db = {}
            minus_ten_db['time_stamp'] = (df.query('schroeder >= -10')[::-1].iloc[0]['time_stamp'] + df.query('schroeder <= -10').iloc[0]['time_stamp'])/2
            minus_ten_db['schroeder']  = (df.query('schroeder >= -10')[::-1].iloc[0]['schroeder']  + df.query('schroeder <= -10').iloc[0]['schroeder'] )/2
            minus_thirtyfive_db = {}
            minus_thirtyfive_db['time_stamp'] = (df.query('schroeder >= -35')[::-1].iloc[0]['time_stamp'] + df.query('schroeder <= -35').iloc[0]['time_stamp'])/2
            minus_thirtyfive_db['schroeder']  = (df.query('schroeder >= -35')[::-1].iloc[0]['schroeder']  + df.query('schroeder <= -35').iloc[0]['schroeder'] )/2

            df_parameter.loc['T30(RT60)', octave['center']] = round(11/6*minus_thirtyfive_db['time_stamp']-5/6*minus_five_db['time_stamp'],2)
            df_parameter.loc['EDT', octave['center']] = round(6*minus_ten_db['time_stamp'],2)
        df_schroeder['time_stamp'] = df_schroeder.index / spl_rate
        df_schroeder = df_schroeder[df_schroeder.index % 10 == 0]
        df_parameter = df_parameter.reset_index()
        df_parameter = df_parameter.rename(columns={'index':'parameter'})
        return [ df_schroeder, df_parameter ]

    def bandpassFilter(self, ir, fs, fbp, filter_type, order, ripple, attenuation):
        nyq = fs / 2.0 
        normalized_cutoff = np.array(fbp) / nyq
        b = []
        a = []
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
