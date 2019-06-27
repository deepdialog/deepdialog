# -*- coding: utf-8 -*-
"""Parse Stories."""
# import os
import yaml
from yaml import Loader


def parse_story(data_path):
    """Parse stories from dir."""
    stories = {}
    # for dirname, _, names in os.walk(data_path):
    #     names = [x for x in names if x.lower().endswith('.yml')]
    #     for name in names:
    #         path = os.path.join(dirname, name)
    obj = yaml.load(open(data_path), Loader=Loader)
    assert isinstance(obj, dict)
    assert 'story' in obj
    for k, v in obj.get('story').items():
        assert k not in stories, 'Story name conflict'
        stories[k] = v
    dialogs = list(stories.values())
    user_intent_list = []
    user_domain_list = []
    user_slot_list = []
    sys_intent_list = []
    sys_slot_list = []
    for dialog in dialogs:
        for turn in dialog:
            assert 'sys' in turn or 'user' in turn, 'Invalid turn'
            assert not ('sys' in turn and 'user' in turn), 'Invalid turn'
            if 'user' in turn:
                domain = ''
                intent = turn['user']
                slots = []
                # 参数
                if '(' in intent:
                    idx = intent.index('(')
                    slot_str = intent[idx + 1:-1].strip()
                    intent = intent[:idx].strip()
                    slots = [
                        x.strip() for x in slot_str.split(',')
                        if x.strip()
                    ]
                    for s in slots:
                        if s not in user_slot_list:
                            user_slot_list.append(s)
                # 分割domain和intent
                if '::' in intent:
                    idx = intent.index('::')
                    domain = intent[:idx].strip()
                    intent = intent[idx + 2:].strip()
                if domain not in user_domain_list:
                    user_domain_list.append(domain)
                if intent not in user_intent_list:
                    user_intent_list.append(intent)
                # 只在domain不为空的时候改变
                if 'domain' not in turn or domain:
                    turn['domain'] = domain
                turn['intent'] = intent
                turn['slots'] = slots
            if 'sys' in turn:
                intent = turn['sys']
                slots = []
                if '(' in intent:
                    idx = intent.index('(')
                    slot_str = intent[idx + 1:-1]
                    intent = intent[:idx]
                    slots = [
                        x.strip() for x in slot_str.split(',')
                        if x.strip()
                    ]
                    for s in slots:
                        if s not in sys_slot_list:
                            sys_slot_list.append(s)
                turn['intent'] = intent
                turn['slots'] = slots
                if intent not in sys_intent_list:
                    sys_intent_list.append(intent)
    return {
        'dialog': dialogs,
        'user_intent': user_intent_list,
        'user_domain': user_domain_list,
        'user_slot': user_slot_list,
        'sys_intent': sys_intent_list,
        'sys_slot': sys_slot_list,
    }
