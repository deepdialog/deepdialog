# -*- coding: utf-8 -*-
"""Dialog State."""

import numpy as np
from copy import deepcopy


class DialogState(object):
    """Dialog State."""

    def __init__(self,
                 user_domain_list,
                 user_intent_list,
                 sys_intent_list,
                 slots,
                 user_domain=None,
                 user_intent=None,
                 sys_intent=None,
                 utterance=None):
        """Init Dialog State."""
        self.user_domain_list = user_domain_list
        self.user_intent_list = user_intent_list
        self.sys_intent_list = sys_intent_list

        self.user_domain_index = {
            None: 0,
        }
        for ui in self.user_domain_list:
            self.user_domain_index[ui] = len(self.user_domain_index)
        self.index_user_domain = {
            v: k
            for k, v in self.user_domain_index.items()
        }

        self.user_intent_index = {
            None: 0,
        }
        for ui in self.user_intent_list:
            self.user_intent_index[ui] = len(self.user_intent_index)
        self.index_user_intent = {
            v: k
            for k, v in self.user_intent_index.items()
        }

        self.sys_intent_index = {
            None: 0,
        }
        for si in self.sys_intent_list:
            self.sys_intent_index[si] = len(self.sys_intent_index)
        self.index_sys_intent = {
            v: k
            for k, v in self.sys_intent_index.items()
        }
        self.slots = deepcopy(slots)
        self.user_domain = user_domain
        self.user_intent = user_intent
        self.sys_intent = sys_intent
        self.utterance = utterance

    def __str__(self):
        """Return stringify state."""
        slots_str = '\n'.join([
            '{}\t{}\t{}'.format(
                x.get('type'),
                x.get('name'),
                x.get('value')
            )
            for x in self.slots
        ])
        return f'''----------
user_domain: {self.user_domain}
user_intent: {self.user_intent}
slots:
{slots_str}
sys_intent: {self.sys_intent}
---------'''

    def clone(self):
        """Clone a state."""
        return DialogState(
            self.user_domain_list,
            self.user_intent_list,
            self.sys_intent_list,
            self.slots,
            self.user_domain,
            self.user_intent,
            self.sys_intent,
            self.utterance
        )

    def __getattr__(self, key):
        """Return certain attribute."""
        if key == 'filled':
            return [0 if x['value'] is None else 1 for x in self.slots]
        if key == 'vec':
            slots_vec = [0 if x['value'] is None else 1 for x in self.slots]
            user_domain_vec = [0] * len(self.user_domain_index)
            user_domain_vec[self.user_domain_index[self.user_domain]] = 1
            user_intent_vec = [0] * len(self.user_intent_index)
            user_intent_vec[self.user_intent_index[self.user_intent]] = 1
            sys_intent_vec = [0] * len(self.sys_intent_index)
            sys_intent_vec[self.sys_intent_index[self.sys_intent]] = 1
            return np.array(np.concatenate([
                user_domain_vec,
                user_intent_vec,
                sys_intent_vec,
                slots_vec
            ]))
        if key == 'slot_vec':
            slots_vec = [0 if x['value'] is None else 1 for x in self.slots]
            return np.array(slots_vec)
        if key == 'user_domain_vec':
            user_domain_vec = [0] * len(self.user_domain_index)
            user_domain_vec[self.user_domain_index[self.user_domain]] = 1
            return np.array(user_intent_vec)
        if key == 'user_intent_vec':
            user_intent_vec = [0] * len(self.user_intent_index)
            user_intent_vec[self.user_intent_index[self.user_intent]] = 1
            return np.array(user_intent_vec)
        if key == 'sys_vec':
            sys_intent_vec = [0] * len(self.sys_intent_index)
            sys_intent_vec[self.sys_intent_index[self.sys_intent]] = 1
            return np.array(sys_intent_vec)
        raise AttributeError(key)

    def __getitem__(self, key):
        """Get certain slot."""
        stype, name = key
        for slot in self.slots:
            if slot['type'] == stype and slot['name'] == name:
                return slot['value']
        raise AttributeError()

    def __setitem__(self, key, value):
        """Set certain slot."""
        stype, name = key
        for slot in self.slots:
            if slot['type'] == stype and slot['name'] == name:
                slot['value'] = value
                return
        raise AttributeError()
