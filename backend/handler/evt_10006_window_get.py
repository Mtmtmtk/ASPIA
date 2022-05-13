
from ducts.spi import EventHandler
import logging
logger = logging.getLogger(__name__)

class Handler(EventHandler):

    def __init__(self):
        super().__init__()

    def setup(self, handler_spec, manager):
        handler_spec.set_description('UK Dissertation')
        try:
            self.evt_spectrogram = manager.get_handler_module('GENERATE_WINDOW')
        except Exception as e:
            import traceback
            traceback.print_exc()
        return handler_spec

    async def handle(self, event):     
        return await self.call(**event.data)

    async def call(self, window_type: str, sampling_points:int):
        window = await self.evt_spectrogram.get_window(window_type, sampling_points)
        return window.tolist()
