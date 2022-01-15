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
        return handler_spec

    async def handle(self, event):     
        return {}

    async def call(self, ir_arr, channels:int):
        np_ir = np.array(ir_arr).T
        reshaped_ir = []
        if channels == 4:
            reshaped_ir = pd.DataFrame(np_ir, columns=['channel_0','channel_1','channel_2','channel_3'])
        elif channels == 2:
            reshaped_ir = pd.DataFrame(np_ir, columns=['channel_0','channel_1'])
        else:
            reshaped_ir = pd.DataFrame(np_ir, columns=['channel_0'])

        average_ir = np.array([])
        if channels == 4:
            average_ir = reshaped_ir['channel_0']
        elif channels == 2:
            average_ir = (reshaped_ir['channel_0']+reshaped_ir['channel_1'])/2
        elif channels == 1:
            average_ir = reshaped_ir['channel_0']

        if np.count_nonzero(np.isnan(average_ir)) != 0:
            average_ir = average_ir.fillna(0)

        average_ir = average_ir / average_ir.abs().max()
        offset_ind = average_ir[average_ir > 0.1].index[0] - 1
        average_ir = average_ir.drop(index=average_ir.index[:offset_ind])
        average_ir = average_ir.reset_index(drop=True)

        return average_ir

