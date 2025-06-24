from .base import *

# LOGGING
# ------------------------------------------------------------------------------
# En producción, enviamos los logs a archivos.
LOGGING['loggers']['django']['handlers'] = ['info_file', 'error_file']
LOGGING['loggers']['']['handlers'] = ['info_file', 'error_file']
