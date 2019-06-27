# -*- coding: utf-8 -*-
"""Train NLU."""

# import os
from ..nlu.nlu import NaturalLanguageUnderstanding
from deepdialog.logger import logger


def train_nlu(data_path, faq_questions=None):
    """Train NLU."""
    # nlu_path = os.path.join(data_path, 'nlu')
    # assert os.path.exists(nlu_path), 'Invalid NLU data path'
    logger.info('Start train NLU')
    nlu = NaturalLanguageUnderstanding()
    nlu.fit(data_path, faq_questions)

    logger.info('\n' + '-' * 30)
    logger.info('NLU Intents:')
    logger.info('\n'.join(nlu.intent_list))
    logger.info('NLU Slots')
    logger.info(nlu.slot_list)

    return nlu
