# -*- coding: utf-8 -*-
"""Train bot.

训练整个机器人
"""

import os
# import sys
import pickle
from .nlu import train_nlu
from .nlg import train_nlg
from .dst import train_dst
from .dpl import train_dpl
from ..faq.faq import FrequentlyAskedQuestions
from ..common.parse_story import parse_story
from ..common.make_init_state import make_init_state
from ..common.build_dialog_train_data import build_dialog_train_data
from deepdialog.logger import logger


def mkdir(path):
    """Make dir if not exists."""
    if not os.path.exists(path):
        os.makedirs(path)


def main(data_path,
         model_path,
         outside_function={},
         n_history=3,
         n_times=50):
    """Train Entrance.

    训练模型
    Args:
        data_path: 数据输入目录
        model_path: 模型输出目录
        outside_function: 外部NLG函数
        n_history: 历史保存轮次
        n_times: 都个story组合轮次
    """
    faq = FrequentlyAskedQuestions()
    faq.fit(data_path)

    # NLU Part
    if len(faq):
        nlu = train_nlu(data_path, faq.questions)
    else:
        nlu = train_nlu(data_path)

    # NLG Part

    nlg = train_nlg(data_path)

    logger.info('\n' + '-' * 30)
    logger.info('NLG Intents:')
    logger.info('\n'.join(nlg.intent_list))

    # story_path = os.path.join(data_path, 'story')
    # parse_story会返回下面这些
    # {
    #     'dialog': dialogs,
    #     'user_intent': user_intent_list,
    #     'user_domain': user_domain_list,
    #     'user_slot': user_slot_list,
    #     'sys_intent': sys_intent_list,
    #     'sys_slot': sys_slot_list,
    # }
    stories = parse_story(data_path)
    # 检查NLU和stories是否冲突
    for ud in stories['user_domain']:
        assert ud in nlu.domain_list, 'user domain {} not in NLU'.format(ud)
    for ui in stories['user_intent']:
        assert ui in nlu.intent_list, 'user intent {} not in NLU'.format(ui)
    for us in stories['user_slot']:
        assert us in nlu.slot_list, 'user slot {} not in NLU'.format(us)
    for si in stories['sys_intent']:
        assert si in nlg.intent_list, 'sys intent {} not in NLG'.format(si)

    init_state = make_init_state(stories)
    (
        x_dst, y_dst,
        x_dpl, y_dpl
    ) = build_dialog_train_data(
        stories['dialog'],
        init_state,
        n_history=n_history,
        n_times=n_times
    )

    # DST Part

    dst = train_dst(x_dst, y_dst)

    # DPL Part
    dpl = train_dpl(x_dpl, y_dpl)

    data = {
        'init_state': init_state,
        'faq': faq,
        'nlu': nlu,
        'nlg': nlg,
        'dst': dst,
        'dpl': dpl,
    }

    model_path_dir = os.path.dirname(model_path)
    mkdir(model_path_dir)
    with open(model_path, 'wb') as fp:
        pickle.dump(data, fp)

    logger.info('\n')
    logger.info('Train done')

    # # Init State
    # state_path = os.path.join(model_path, 'init_state.model')
    # mkdir(model_path)
    # with open(state_path, 'wb') as fp:
    #     pickle.dump(init_state, fp)

    # # Save
    # mkdir(model_path)
    # faq_output = os.path.join(model_path, 'faq.model')
    # with open(faq_output, 'wb') as fp:
    #     pickle.dump(faq, fp)
    # nlu_output = os.path.join(model_path, 'nlu.model')
    # with open(nlu_output, 'wb') as fp:
    #     pickle.dump(nlu, fp)
    # nlg_output = os.path.join(model_path, 'nlg.model')
    # with open(nlg_output, 'wb') as fp:
    #     pickle.dump(nlg, fp)
    # dst_output = os.path.join(model_path, 'dst.model')
    # with open(dst_output, 'wb') as fp:
    #     pickle.dump(dst, fp)
    # dpl_output = os.path.join(model_path, 'dpl.model')
    # with open(dpl_output, 'wb') as fp:
    #     pickle.dump(dpl, fp)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Train DeepDialog Model')
    parser.add_argument(
        'data_path', type=str)
    parser.add_argument(
        'model_path', type=str)
    args = parser.parse_args()
    main(args.data_path, args.model_path)
