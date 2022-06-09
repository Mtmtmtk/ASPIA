from ducts.spi import EventHandler
import logging
logger = logging.getLogger(__name__)

class Handler(EventHandler):

    def __init__(self):
        super().__init__()

    def setup(self, handler_spec, manager):
        handler_spec.set_description('UK Dissertation')
        try:
            self.evt_acoustic_parameters = manager.get_handler_module('CALCULATE_ACOUSTIC_PARAMETERS')
        except Exception as e:
            import traceback
            traceback.print_exc()
        return handler_spec

    async def handle(self, event):     
        return await self.call(**event.data)

    async def call(self, spl_rate: int, filter_type: str, order: int, ripple:int = 5, attenuation:int = 5):
        df_paramters = await self.evt_acoustic_parameters.get_parameters(spl_rate, filter_type, order, ripple, attenuation)
        return df_paramters.to_dict('records')
