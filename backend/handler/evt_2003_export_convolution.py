from ducts.spi import EventHandler
import logging
logger = logging.getLogger(__name__)

class Handler(EventHandler):

    def __init__(self):
        super().__init__()

    def setup(self, handler_spec, manager):
        print('setup')
        handler_spec.set_description('UK Dissertation')
        try:
            print('trying')
            self.evt_convolution = manager.get_handler_module('CONVOLUTE')
            print(self.evt_convolution)
        except Exception as e:
            import traceback
            traceback.print_exc()
        return handler_spec

    async def handle(self, event):     
        print('handling')
        return await self.call(**event.data)

    async def call(self, recording, sampling_rate: int, path:str, output_channels: str):
        print('printing')
        return await self.evt_convolution.call(recording, sampling_rate, path, output_channels)
