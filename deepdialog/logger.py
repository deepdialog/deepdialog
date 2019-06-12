# -*- coding: utf-8 -*-
"""DeepDialog logger."""

import os
import sys
import logging

LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
MAPPING = {
    'INFO': logging.INFO,
    'DEBUG': logging.DEBUG,
    'ERROR': logging.ERROR,
    'WARNING': logging.WARNING
}
assert LOG_LEVEL in MAPPING
LEVEL = MAPPING[LOG_LEVEL]


logger = logging.getLogger('deepdialog')
logger.setLevel(LEVEL)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(LEVEL)
# create formatter and add it to the handlers
formatter = logging.Formatter(
    '%(levelname)s %(asctime)s %(module)s %(message)s')
ch.setFormatter(formatter)
# add the handlers to logger
logger.addHandler(ch)

stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setFormatter(formatter)
stdout_handler.setLevel(LEVEL)
logger.addHandler(stdout_handler)
