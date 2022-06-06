from ducts.spi import EventHandler
import logging
logger = logging.getLogger(__name__)

class Handler(EventHandler):

    def __init__(self):
        super().__init__()

    def setup(self, handler_spec, manager):
        handler_spec.set_description('UK Dissertation')
        try:
            self.evt_filter_spectrum = manager.get_handler_module('CALCULATE_FILTER_SPECTRUM')
        except Exception as e:
            import traceback
            traceback.print_exc()
        return handler_spec

    async def handle(self, event):     
        return await self.call(**event.data)

    async def call(self, spl_rate: int, filter_type: str, order: int):
        ret = await self.evt_filter_spectrum.create_filter_spectrum(spl_rate, filter_type, order)
        ret[0] = ret[0].to_dict(orient='list') 
        ret[1] = ret[1].tolist()
        return ret
