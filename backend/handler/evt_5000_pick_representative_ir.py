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
        return handler_spec

    async def handle(self, event):     
        return {}

    async def call(self, ir_df: pd.DataFrame):
        channels = len(ir_df.columns)
        average_ir = np.array([])
        if (channels == 4) or (channels == 1):
            average_ir = ir_df.iloc[:,0]
        elif channels == 2:
            average_ir = (ir_df.iloc[:, 0] + ir_df.iloc[:, 1])/2

        if np.count_nonzero(np.isnan(average_ir)) != 0:
            average_ir = average_ir.fillna(0)

        average_ir = average_ir / average_ir.abs().max()
        offset_ind = average_ir[average_ir > 0.1].index[0] - 1
        average_ir = average_ir.drop(index=average_ir.index[:offset_ind])
        average_ir = average_ir.reset_index(drop=True)

        return average_ir

