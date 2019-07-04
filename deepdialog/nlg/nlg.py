# -*- coding: utf-8 -*-
"""NLG Module."""

import os
import random
import yaml
from yaml import Loader
from ..common.system_action import SystemAction
from ..common.dialog_state import DialogState
from ..common.component import Component
from .ext_sysact import load_ext


class NaturalLanguageGenerator(Component):
    """NLG Module."""

    def __init__(self, outside_function={}):
        """Init NLG."""
        self.intent_list = []
        self.slot_list = []
        self.mapping = {}
        self.outside_function = outside_function

    def fit(self, data_path):
        """Fit the model."""
        assert os.path.exists(data_path)
        data = {}
        # for dirname, _, names in os.walk(data_path):
        #     names = [x for x in names if x.lower().endswith('.yml')]
        #     for name in names:
        #         path = os.path.join(dirname, name)
        obj = yaml.load(open(data_path), Loader=Loader)
        assert 'nlg' in obj
        for item in obj.get('nlg'):
            assert 'sysact' in item
            assert 'response' in item
            k, v = item.get('sysact'), item.get('response')
            assert k not in data
            if v == 'ext':
                data[k] = ('func', k)
            else:
                data[k] = v
        self.mapping = data
        self.intent_list = sorted(data.keys())
        assert 'None' in self.mapping, \
            '应该有一个名为None的intent在NLG中，为了响应未知情况'

    def forward(self, state: DialogState, sys_action: SystemAction) -> str:
        """Predict."""
        assert (
            sys_action.intent is None
            or sys_action.intent in self.mapping
        ), 'sys_action {} not exists in mapping'.format(sys_action.intent)
        if sys_action.intent is None:
            response = self.mapping['None']
        else:
            response = self.mapping[sys_action.intent]
        if isinstance(response, list):
            utterance = random.choice(response)
        elif isinstance(response, tuple) \
                and len(response) == 2 and response[0] == 'func':
            func = load_ext(response[1])
            utterance = func(state)
            # utterance = self.outside_function[response[1]](state)
        elif isinstance(response, str):
            utterance = response
        else:
            raise RuntimeError('Invalid response')
        return utterance
