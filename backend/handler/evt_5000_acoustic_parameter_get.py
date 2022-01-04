from ducts.spi import EventHandler
import numpy as np
import pandas as pd
from matplotlib import pyplot
from scipy import signal
import logging
logger = logging.getLogger(__name__)

class Handler(EventHandler):

    def __init__(self):
        super().__init__()

    def setup(self, handler_spec, manager):
        handler_spec.set_description('UK Dissertation')
        self.evt_reshape_ir = manager.get_handler_module('RESHAPE_IR')
        self.octave_band = [
            { 'center': '31.5', 'band':[22   ,44] },
            { 'center': '63'  , 'band':[44   ,88] },
            { 'center': '125' , 'band':[88   ,177] },
            { 'center': '250' , 'band':[177  ,355] },
            { 'center': '500' , 'band':[355  ,710] },
            { 'center': '1k'  , 'band':[710  ,1420] },
            { 'center': '2k'  , 'band':[1420 ,2840] },
            { 'center': '4k'  , 'band':[2840 ,5680] },
            { 'center': '8k'  , 'band':[5680 ,11360] },
            { 'center': '16k' , 'band':[11360,22049] },
        ]
        return handler_spec

    async def handle(self, event):     
        return await self.call(**event.data)

    async def call(self, ir_arr, spl_rate: int, channels:int):
        np_ir = np.array(ir_arr).T
        reshaped_ir = []
        if channels == 4:
            reshaped_ir = pd.DataFrame(np_ir, columns=['channel_0','channel_1','channel_2','channel_3'])
        elif channels == 2:
            reshaped_ir = pd.DataFrame(np_ir, columns=['channel_0','channel_1'])
        else:
            reshaped_ir = pd.DataFrame(np_ir, columns=['channel_0'])
        print(reshaped_ir)

        average = []
        if channels == 4:
            average = reshaped_ir['channel_0']
        elif channels == 2:
            average = (reshaped_ir['channel_0']+reshaped_ir['channel_1'])/2
        elif channels == 1:
            average = reshaped_ir['channel_0']

        average = average.fillna(0)

        df_parameter = pd.DataFrame(0, columns=['31.5','63','125','250','500','1k','2k','4k','8k','16k'], index=['T30(RT60)','EDT','D50','C50','C80'])
        for octave in self.octave_band:
            fe1 = octave['band'][0]
            fe2 = octave['band'][1]
            order = 3
            filtered_signal = self.bandpassFilter(average, spl_rate, fe1, fe2, order)
            sr_filtered_signal = pd.Series(filtered_signal)


            D_fifty  = round(np.sum(sr_filtered_signal[:int(0.05*spl_rate)]**2)/np.sum(sr_filtered_signal**2), 2)
            C_fifty  = round(10 * np.log10(np.sum(sr_filtered_signal[:int(0.05*spl_rate)]**2)/np.sum(sr_filtered_signal[int(0.05*spl_rate):]**2)), 2)
            C_eighty = round(10 * np.log10(np.sum(sr_filtered_signal[:int(0.08*spl_rate)]**2)/np.sum(sr_filtered_signal[int(0.08*spl_rate):]**2)), 2)
            df_parameter.loc['D50',octave['center']] = D_fifty
            df_parameter.loc['C50',octave['center']] = C_fifty
            df_parameter.loc['C80',octave['center']] = C_eighty


            df = pd.DataFrame(columns=['energy','sum_energy','schroeder','time_stamp'])
            df['energy'] = sr_filtered_signal**2
            total_energy = np.sum(df['energy'])
            energy_cumsum = np.cumsum(df['energy'])
            energy_cumsum = np.append(0, energy_cumsum)
            energy_cumsum = np.delete(energy_cumsum, -1)
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

    def bandpassFilter(self, ir, fs, fe1, fe2, order):
        nyquist = fs / 2.0
        b,a = signal.butter(1, [fe1/nyquist, fe2/nyquist], btype='band')
        for i in range(0,order):
            ir = signal.filtfilt(b,a,ir)
        return ir
