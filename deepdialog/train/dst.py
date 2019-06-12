# -*- coding: utf-8 -*-
"""Train DST."""

from ..dst.dst import DialogStateTracker
from deepdialog.logger import logger


def train_dst(x_dst, y_dst):
    """Train DST."""
    dst = DialogStateTracker()
    dst.fit(x_dst, y_dst)

    logger.info('\n' + '-' * 30)
    logger.info('DST: trained')
    return dst
