from enum import IntEnum
class ForecastStatus(IntEnum):
    IDLE                    = 0
    IMPORT_IR               = 20
    START_DOWNLOAD          = 30
    CREATE_ANECHOIC_SOUND   = 40
    ANECHOIC_SOUND_FINISHED = 50
    RESAMPLE_FILES          = 60
    START_CONVOLUTION       = 70
    CONVOLUTION_FINISHED    = 80
