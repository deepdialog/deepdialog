# -*- coding: utf-8 -*-
"""NLU Module."""

import numpy as np
from tqdm import tqdm
from ..common.user_action import UserAction
from .load_nlu_data import load_nlu_data
from .data_to_iob import data_to_iob
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from .slot_filler import NERSlotFiller
from deepdialog.logger import logger
from .keras_intent import get_model
from sklearn.preprocessing import LabelBinarizer
from deepdialog.common import FAQ_INTENT
from keras.utils import to_categorical
from ..common.component import Component


class NaturalLanguageUnderstanding(Component):
    """NLU Module."""

    def __init__(self):
        """Init."""
        self.tokenizer = None
        self.intent_clr = None
        self.domain_clr = None
        self.intent_label = None
        self.domain_label = None
        self.ner_slot = None
        self.slot_list = []
        self.intent_list = []
        self.domain_list = []
        self.vocab_size = 10000
        self.maxlen = 50

    def fit(self, data_path, faq_questions=None):
        """Fit NLU Module.

        先从目录转换出所有的yml文件
        然后得到四个列表，分别是句子本身，槽，领域，意图，他们的长度是相等的
        例如一条句子：
        sentences: [ ['我', '爱', '你'] ]
        slots: [ 'O', 'O', 'O' ]
        domains: [ 'life' ]
        intents: [ 'ask_love' ]
        """
        raw_intents, raw_entities = load_nlu_data(data_path)
        sentences, slots, domains, intents = data_to_iob(
            raw_intents, raw_entities)

        slot_list = []
        for slot in slots:
            for s in slot:
                if s.startswith('B_'):
                    if s[2:] not in slot_list:
                        slot_list.append(s[2:])
        self.slot_list = sorted(set(slot_list))

        # 处理特殊的FAQ意图
        if faq_questions is None:
            faq_questions = []
        else:
            faq_questions = [
                list(x)
                for x in faq_questions
            ] * 10
            # TODO 一个不太好的超参，控制FAQ和其他对话的训练比例

        # import pdb; pdb.set_trace()
        # Entity as B, I as * 2 + Outer
        self.ner_slot = NERSlotFiller(len(self.slot_list) * 2 + 1)

        self.ner_slot.fit(sentences, slots)

        slot_accuracy, _ = self.ner_slot.eval(
            sentences,
            slots
        )

        self.intent_label = LabelBinarizer()
        self.intent_label.fit(intents + [FAQ_INTENT])

        self.domain_label = LabelBinarizer()
        self.domain_label.fit(domains + [FAQ_INTENT])

        self.intent_list = self.intent_label.classes_.tolist()
        self.domain_list = self.domain_label.classes_.tolist()

        self.tokenizer = Tokenizer(num_words=self.vocab_size, char_level=True)
        self.tokenizer.fit_on_texts(sentences + faq_questions)

        seq = self.tokenizer.texts_to_sequences(sentences + faq_questions)
        seq_pad = pad_sequences(seq, maxlen=self.maxlen)

        self.intent_clr = get_model(
            self.intent_label.classes_.shape[0], n_vocab=self.vocab_size)
        self.domain_clr = get_model(
            self.domain_label.classes_.shape[0], n_vocab=self.vocab_size)

        y_intent = self.intent_label.transform(
            intents + [FAQ_INTENT] * len(faq_questions))
        y_domain = self.domain_label.transform(
            domains + [FAQ_INTENT] * len(faq_questions))
        if 1 == y_domain.shape[1]:
            y_domain = to_categorical(y_domain, 2)

        self.intent_clr.fit(seq_pad, y_intent)
        self.domain_clr.fit(seq_pad, y_domain)

        loop = tqdm(zip(
            sentences, domains, intents),
            total=len(sentences))

        domain_ret = self.domain_label.inverse_transform(
            self.domain_clr.predict_proba(seq_pad))
        intent_ret = self.intent_label.inverse_transform(
            self.intent_clr.predict_proba(seq_pad))

        ret = []
        for (a, b, c), dr, ir in zip(loop, domain_ret, intent_ret):
            ret.append((
                b == dr,
                c == ir
            ))
        domain_accuracy, intent_accuracy = (
            np.sum([x[0] for x in ret]) / len(sentences),
            np.sum([x[1] for x in ret]) / len(sentences)
        )
        logger.info(
            'domain_accuracy: %s\n' +
            'intent_accuracy: %s\n' +
            'slot_accuracy: %s\n',
            domain_accuracy,
            intent_accuracy,
            slot_accuracy
        )

    def forward(self, utterance: str) -> UserAction:
        """Predict sentence."""
        user_action = UserAction(utterance)
        seq = self.tokenizer.texts_to_sequences([user_action.raw['tokens']])
        seq_pad = pad_sequences(seq, maxlen=self.maxlen)
        user_action.raw['intent'] = self.intent_label.inverse_transform(
            self.intent_clr.predict_proba(seq_pad))[0]
        user_action.raw['domain'] = self.domain_label.inverse_transform(
            self.domain_clr.predict_proba(seq_pad))[0]
        user_action.raw = self.ner_slot.predict_slot(user_action.raw)
        print('user_action', user_action.raw)
        return user_action
