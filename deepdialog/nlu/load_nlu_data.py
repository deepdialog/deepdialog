# -*- coding: utf-8 -*-
"""Load NLU Data.

python3 -m nlu.utils.data_loader
"""

import os
import yaml
from yaml import Loader
from deepdialog.logger import logger


def load_nlu_data(data_path):
    """Load NLU data from dir.

    目录中应该有intents与entities子目录，分别保存意图和实体信息，为yaml格式
    """
    assert os.path.exists(data_path), '数据“{}”不存在'.format(data_path)

    # paths = []
    # for dirname, _, filenames in os.walk(data_dir):
    #     filenames = [x for x in filenames if x.endswith('.yml')]
    #     for filename in filenames:
    #         path = os.path.join(dirname, filename)
    #         paths.append(path)

    # assert paths, '找不到yaml数据文件，注意要以“.yml”后缀名结尾'

    entities = []
    intents = []

    # for path in paths:
    with open(data_path, 'r') as fp:
        try:
            obj = yaml.load(fp, Loader=Loader)
        except:  # noqa
            raise Exception('数据读取错误，可能不是合法YAML文件 “{}”'.format(data_path))
        assert 'nlu' in obj
        objs = obj.get('nlu')
        assert isinstance(objs, (list, tuple)), \
            '数据文件必须是list or tuple “{}”'.format(data_path)

        for obj in objs:
            if isinstance(obj, dict):
                if 'intent' in obj:
                    assert 'data' in obj, \
                        '意图必须包括“data”属性 “{}”'.format(data_path)
                    assert isinstance(obj['data'], (list, tuple)) \
                        and obj['data'], \
                        '意图必须包括“data”且长度大于0 “{}”'.format(data_path)
                    intents.append(obj)
                elif 'entity' in obj:
                    assert 'data' in obj, \
                        '实体必须包括“data”属性 “{}”'.format(data_path)
                    assert 'copyFrom' in obj or (
                        isinstance(obj['data'], (list, tuple)) and obj['data']
                    ), '有copyFrom，或者有“data”且长度大于0 “{}”'.format(data_path)
                    entities.append(obj)

    entities = entity_merge(entities)

    logger.info(
        '读取到了 %s 个intent， %s 个entity',
        len(intents), len(entities))

    return intents, entities


def entity_merge(entities):
    """Merge entities."""
    entity_index = {}
    for obj in entities:
        entity = obj['entity']
        data = obj['data']
        if entity not in entity_index:
            entity_index[entity] = {'entity': entity, 'data': []}
        entity_index[entity]['data'] += data
        if 'regex' in obj and isinstance(obj['regex'], str) and obj['regex']:
            entity_index[entity]['regex'] = obj['regex']
        if 'copyFrom' in obj and isinstance(obj['copyFrom'],
                                            str) and obj['copyFrom']:
            entity_index[entity]['copyFrom'] = obj['copyFrom']
    for v in entity_index.values():
        if 'copyFrom' in v and v['copyFrom'] in entity_index:
            v['data'] += entity_index[v['copyFrom']]['data']
    return list(entity_index.values())
