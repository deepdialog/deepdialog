# -*- coding: utf-8 -*-
"""Build train data."""

import random
import numpy as np
from deepdialog.logger import logger


def make_new_state(state, domain, intent, slots, utterance=''):
    """Make new state.

    根据输入的状态，用户输入的信息，得到一个新的state
    """
    new_state = state.clone()
    new_state.user_domain = domain
    new_state.user_intent = intent
    new_state.utterance = utterance
    new_state.sys_intent = None
    filled = []
    for slot in slots:
        if isinstance(slot, str):
            slot_name = slot
            value = 1
        else:
            slot_name = slot['slot_name']
            value = slot['slot_value']
        if intent.startswith('request'):
            stype = 'requestable'
        else:
            stype = 'informable'
        filled.append(slot_name)
        new_state[(stype, slot_name)] = value
    # for slot in new_state.slots:
    #     if slot['type'] == 'informable' \
    #             and slot['name'] not in filled:
    #         slot['value'] = None
    #     elif slot['type'] == 'requestable' \
    #             and slot['name'] not in filled:
    #         slot['value'] = None
    return new_state


def build_dialog_train_data(dialogs, init_state, n_history, n_times):
    """Generate Trainning Data, include DST and DPL."""
    x_dst, y_dst = [], []
    x_dpl, y_dpl = [], []

    dialog_queue = []
    for i in range(len(dialogs) * 1000):
        dialog_queue.append('clean')
        for i in range(5):
            dialog_queue.append(random.choice(dialogs))
    logger.info('dialog_queue length %s', len(dialog_queue))

    history = []
    for i in range(n_history):
        history.append(init_state.clone())

    for dialog in dialog_queue:
        if dialog == 'clean':
            history = []
            for i in range(n_history):
                history.append(init_state.clone())
            continue
        for turn_ind, turn in enumerate(dialog):
            state = history[-1].clone()  # last history
            if 'user' in turn:

                new_state = make_new_state(
                    init_state.clone(),
                    turn['domain'],
                    turn['intent'],
                    turn['slots']
                )

                y = np.array([
                    1 if b > 0 else 0
                    for a, b in zip(
                        state.slot_vec.tolist(),
                        new_state.slot_vec.tolist()
                    )
                ])

                state.user_intent = new_state.user_intent
                state.user_domain = new_state.user_domain
                state.utterance = new_state.utterance
                for i, slot in enumerate(new_state.slots):
                    if y[i] > 0.5:
                        state.slots[i] = slot

                x = np.array([history[-1].vec] + [new_state.vec])
                x_dst.append(x)
                y_dst.append(y)
                if np.sum(y) > 0:
                    for i in range(10):
                        x_dst.append(x)
                        y_dst.append(y)

                history = history[1:] + [state]
            if 'sys' in turn:
                x = np.array([s.vec for s in history])
                state.sys_intent = turn['intent']  # 设置为了获取y向量，不影响history
                y = state.sys_vec
                x_dpl.append(x)
                y_dpl.append(y)
                history[-1].sys_intent = turn['intent']  # 设置history

    x_dst = np.array(x_dst)
    y_dst = np.array(y_dst)
    x_dpl = np.array(x_dpl)
    y_dpl = np.array(y_dpl)
    logger.info(
        'dialog train data, x_dst %s y_dst %s x_dpl %s y_dpl %s',
        x_dst.shape, y_dst.shape, x_dpl.shape, y_dpl.shape)
    return x_dst, y_dst, x_dpl, y_dpl
