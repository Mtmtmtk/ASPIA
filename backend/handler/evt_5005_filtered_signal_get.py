from ducts.spi import EventHandler
import logging
logger = logging.getLogger(__name__)

class Handler(EventHandler):

    def __init__(self):
        super().__init__()

    def setup(self, handler_spec, manager):
        handler_spec.set_description('UK Dissertation')
        try:
            self.evt_filtered_signal = manager.get_handler_module('CALCULATE_FILTERED_SIGNAL')
        except Exception as e:
            import traceback
            traceback.print_exc()
        return handler_spec

    async def handle(self, event):     
        return await self.call(**event.data)

    async def call(self, spl_rate: int, filter_type: str, order: int, ripple:int = 5, attenuation:int = 5):
        signal_dict =  await self.evt_filtered_signal.filter_signal(spl_rate, filter_type, order, ripple, attenuation)
        output_dict = {
            '31.5': [],
            '63'  : [],
            '125' : [],
            '250' : [],
            '500' : [],
            '1k'  : [],
            '2k'  : [],
            '4k'  : [],
            '8k'  : [],
            '16k' : [],
        }
        for octave, df in signal_dict.items():
            for channel in df.columns:
                output_dict[octave].append(df[channel].tolist())
        return output_dict
