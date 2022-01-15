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

    async def call(self, ir_arr, spl_rate: int, channels:int):
        average_ir = await self.evt_pick_representative_ir.call(ir_arr,channels)

        df_output = pd.DataFrame(columns=['31.5','63','125','250','500','1k','2k','4k','8k','16k','time_stamp'])
        for octave in self.octave_band:
            fbp = octave['bandpass']
            order = 3
            filtered_ir = self.bandpassFilter(average_ir, spl_rate, fbp, order)
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
        return df_output.to_dict(orient='list')

    def bandpassFilter(self, ir, fs, fbp, order):
        nyquist = fs / 2.0
        normalized_cutoff = np.array(fbp) / nyquist
        b,a = signal.butter(order, normalized_cutoff, btype='band', analog=False)
        filtered_ir = signal.lfilter(b,a,ir)
        return filtered_ir
