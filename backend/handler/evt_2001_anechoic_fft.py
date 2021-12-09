from ducts.spi import EventHandler

import logging
logger = logging.getLogger(__name__)

class Handler(EventHandler):

    def __init__(self):
        super().__init__()

    def setup(self, handler_spec, manager):
        handler_spec.set_description('UK Dissertation')
        try:
        except Exception as e:
            import traceback
            traceback.print_exc()
        return handler_spec

    async def handle(self, event):     
        return 0

    async def call(self, recording, ir):
        anechoic_data = recording
        anechoic_sr = 48000
        anechoic_fft = np.fft.fft(anechoic_data, n=len(anechoic_data))
        return anechoic_fft 
