# -*- coding: utf-8 -*-
"""Data utils.

python3 -m nlu.utils.data_iob
"""

import re
import numpy as np
from sklearn.utils import shuffle
from joblib import Parallel, delayed
from deepdialog.logger import logger

SPLITOR = '|'


def get_index_entities_data(entities):
    """Entity utils."""
    ret = {}
    for x in entities:
        data = []
        for item in x['data']:
            if isinstance(item, str):
                data.append(item)
            elif isinstance(item, list):
                for iitem in item:
                    if isinstance(iitem, str):
                        data.append(iitem)
        if x['entity'] not in ret:
            ret[x['entity']] = []
        ret[x['entity']] += data
    for k, v in ret.items():
        ret[k] = shuffle(v)
    return ret


def fill_iob(slot_name, slot_value):
    """Fill IOB.

    填充IOB格式
    call: fill_iob('date', '2018')
    result: ['B_date', 'I_date', 'I_date', 'I_date', 'I_date']
    Args:
        slot_name: 槽值名称
        slot_value: 槽值结果
    """
    b_tag = 'B_{}'.format(slot_name)
    i_tag = 'I_{}'.format(slot_name)
    return [b_tag] + ([i_tag] * (len(slot_value) - 1))


def convert_item(intent, index_entities_data, slot_count):
    """Convert item."""
    slot_name_index = {}

    def _choice(slot_name):
        if slot_name not in slot_name_index:
            slot_name_index[slot_name] = 0
        if slot_name_index[slot_name] >= len(index_entities_data[slot_name]):
            slot_name_index[slot_name] = 0
        value = index_entities_data[slot_name][slot_name_index[slot_name]]
        slot_name_index[slot_name] += 1
        return value

    (sentence_results, slot_results, domain_results,
     intent_results) = [], [], [], []

    loop = [10]
    for item in intent['data']:
        if 'name' in item:
            slot_name = item['name']
            assert slot_name in index_entities_data
            loop.append(
                int(min(7000, len(index_entities_data[slot_name]))
                    )  # / slot_count[slot_name])
            )

    loop = max(loop)
    llen = len(
        re.findall(r'\|', ' '.join([x['text'] for x in intent['data']])))
    if llen > 0:
        loop *= llen

    for _ in range(loop):

        sentence_result = []
        slot_result = []

        for i, item in enumerate(intent['data']):
            if 'name' in item:
                slot_name = item['name']
                slot_value = _choice(slot_name)

                sentence_result += list(slot_value)
                slot_result += fill_iob(slot_name, slot_value)
            else:
                text = item['text']
                # 转换 [[要|想要]] => 随机一个
                text = re.sub(
                    r'\[\[([^\]]+)\]\]', lambda x: np.random.choice(
                        x.group(1).split('|')), text)
                sentence_result += list(text)
                slot_result += ['O'] * len(text)

        domain_result = str(intent['domain'])
        intent_result = str(intent['intent'])

        sentence_results.append(sentence_result)
        slot_results.append(slot_result)
        domain_results.append(domain_result)
        intent_results.append(intent_result)

    return sentence_results, slot_results, domain_results, intent_results


def data_to_iob(intents, entities):
    """Convert Data to IOB Format.

    把数据转换为IOB格式
    Inside-outside-beginning
    """
    np.random.seed(0)
    index_entities_data = get_index_entities_data(entities)

    slot_count = {}
    for intent in intents:
        for item in intent['data']:
            if 'name' in item:
                slot_name = item['name']
                if slot_name not in slot_count:
                    slot_count[slot_name] = 0
                slot_count[slot_name] += 1

    sentence_result, slot_result, domain_result, intent_result = [], [], [], []

    logger.info(f'parallel job %s', len(intents))
    ret = Parallel(
        n_jobs=-1, verbose=6)(
            delayed(convert_item)(intent, index_entities_data, slot_count)
            for intent in intents)

    logger.info('parallel job done')

    for r1, r2, r3, r4 in ret:
        sentence_result += r1
        slot_result += r2
        domain_result += r3
        intent_result += r4

    logger.info('return IOB data')
    return sentence_result, slot_result, domain_result, intent_result
