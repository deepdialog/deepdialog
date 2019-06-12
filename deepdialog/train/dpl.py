# -*- coding: utf-8 -*-
"""Train DPL."""

from ..dpl.dpl import DialogPolicyLearning
from deepdialog.logger import logger


def train_dpl(x_dpl, y_dpl):
    """Train DPL."""
    dpl = DialogPolicyLearning()
    dpl.fit(x_dpl, y_dpl)

    logger.info('\n' + '-' * 30)
    logger.info('DPL: trained')
    return dpl
