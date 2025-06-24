from .base import *

# LOGGING
# ------------------------------------------------------------------------------
# Sobrescribimos los handlers para que todo vaya a la consola en desarrollo
LOGGING['loggers']['django']['handlers'] = ['console']
LOGGING['loggers']['']['handlers'] = ['console']