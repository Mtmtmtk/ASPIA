from ducts.spi import EventHandler
import numpy as np
import pandas as pd
from matplotlib import pyplot
import logging
from scipy import signal
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
        #reshaped_ir = await self.evt_reshape_ir.call(ir_arr, spl_rate, channels)
        np_ir = np.array(ir_arr).T
        reshaped_ir = []
        if channels == 4:
            reshaped_ir = pd.DataFrame(np_ir, columns=['channel_0','channel_1','channel_2','channel_3'])
        elif channels == 2:
            reshaped_ir = pd.DataFrame(np_ir, columns=['channel_0','channel_1'])
        else:
            reshaped_ir = pd.DataFrame(np_ir, columns=['channel_0'])
        print(reshaped_ir)

        average_ir = []
        if channels == 4:
            average_ir = reshaped_ir['channel_0']
        elif channels == 2:
            average_ir = (reshaped_ir['channel_0']+reshaped_ir['channel_1'])/2
        elif channels == 1:
            average_ir = reshaped_ir['channel_0']

        average_ir = average_ir.fillna(0)

        df_output = pd.DataFrame(columns=['31.5','63','125','250','500','1k','2k','4k','8k','16k','time_stamp'])
        for octave in self.octave_band:
            fe1 = octave['band'][0]
            fe2 = octave['band'][1]
            order = 3
            filtered_ir = self.bandpassFilter(average_ir, spl_rate, fe1, fe2, order)
            sr_filtered_ir = pd.Series(filtered_ir)

            df = pd.DataFrame(columns=['energy','sum_energy','schroeder(db)'])
            df['energy'] = filtered_ir**2

            total_energy = np.sum(df['energy'])
            energy_cumsum = np.cumsum(df['energy'])
            energy_cumsum = np.append(0, energy_cumsum)
            energy_cumsum = np.delete(energy_cumsum, -1)

            df['sum_energy'] = total_energy - energy_cumsum
            df['schroeder(db)'] = 10 * np.log10(df['sum_energy']/total_energy)
            df_output[octave['center']] = df['schroeder(db)']
        df_output['time_stamp'] = df_output.index / spl_rate

        df_output = df_output[df_output.index % 10 == 0]
        print(df_output)
        return df_output.to_dict(orient='list')

    def bandpassFilter(self, ir, fs, fe1, fe2, order):
        nyquist = fs / 2.0
        b,a = signal.butter(1, [fe1/nyquist, fe2/nyquist], btype='band')
        for i in range(0,order):
            ir = signal.filtfilt(b,a,ir)
        return ir
