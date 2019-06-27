# -*- coding: utf-8 -*-
"""Slot extraction.

python3 -m lu.engine.ner_slot_filler
"""

# import os
# from deepdialog.logger import logger

from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.utils import to_categorical
from .keras_ner import get_model


def get_slots(sentence, slot):
    """Extract Slots."""
    current = None
    current_str = []
    ret = []
    for s, ss in zip(sentence, slot):
        if ss != 'O':
            ss = ss[2:]
            if current is None:
                current = ss
                current_str = [s]
            else:
                if current == ss:
                    current_str.append(s)
                else:
                    ret.append((current, ''.join(current_str)))
                    current = ss
                    current_str = []
        else:

            # 应对 B1 O B1 的情况，B1和B1很可能是连续的，而O是空格
            if (s == ' ' or s == '　'):
                continue

            if current is not None:
                ret.append((current, ''.join(current_str)))
                current = None
                current_str = []

    if current is not None:
        ret.append((current, ''.join(current_str)))

    ret_dict = {}
    for s, v in ret:
        if s not in ret_dict:
            ret_dict[s] = []
        ret_dict[s].append(v)
    return ret_dict


def get_slots_detail(sentence, slot):
    """Get sentence slot detail.

    example:
    sentence == ['买', '2', '手']
    slot == ['O', 'B_number', 'O']
    """
    current = None
    current_str = []
    ret = []
    i = 0
    for i, (s, ss) in enumerate(zip(sentence, slot)):
        if ss != 'O':
            ss = ss[2:]
            if current is None:
                current = ss
                current_str = [s]
            else:
                if current == ss:
                    current_str.append(s)
                else:
                    ret.append((current, ''.join(current_str),
                                i - len(current_str), i))
                    current = ss
                    current_str = [s]
        else:
            if current is not None:
                ret.append((current, ''.join(current_str),
                            i - len(current_str), i))
                current = None
                current_str = []

    if current is not None:
        ret.append((current, ''.join(current_str), i - len(current_str), i))

    ret_list = []
    for s, v, start, end in ret:
        ret_list.append({'slot_name': s, 'slot_value': v, 'pos': (start, end)})
    return ret_list


def get_exact_right(slot_true, slot_pred):
    """Extract Ground Truth."""
    import json
    for s, v in slot_true.items():
        if s not in slot_pred:
            return False
        v = json.dumps(v)
        vp = json.dumps(slot_pred[s])
        if v != vp:
            return False
    return True


class NERSlotFiller(object):
    """NER Slot Classifier."""

    def __init__(self, label_size, maxlen=50, vocab_size=10000):
        """Init."""
        self.ner = None
        self.label_size = label_size
        self.maxlen = maxlen
        self.vocab_size = vocab_size

    def fit(self,
            sentence_result,
            slot_result,
            epochs=40):
        """Fit model."""
        self.tokenizer = Tokenizer(
            num_words=self.vocab_size, char_level=True, lower=False)
        self.tokenizer.fit_on_texts(sentence_result)
        seq = self.tokenizer.texts_to_sequences(sentence_result)
        seq_pad = pad_sequences(seq, maxlen=self.maxlen)

        # import pdb; pdb.set_trace()
        self.tokenizer_y = Tokenizer(
            num_words=self.label_size+1, char_level=True, lower=False)
        self.tokenizer_y.fit_on_texts(slot_result)
        seq_y = self.tokenizer_y.texts_to_sequences(slot_result)
        seq_pad_y = pad_sequences(seq_y, maxlen=self.maxlen)
        # For CRF
        # seq_pad_y = seq_pad_y.reshape(
        #     seq_pad_y.shape[0], seq_pad_y.shape[1], 1)
        # For Softmax
        seq_pad_y = to_categorical(seq_pad_y)

        self.ner = get_model(n_output=self.label_size+1)
        self.ner.model.fit(
            seq_pad,
            seq_pad_y,
            epochs=epochs)

    def predict_slot(self, nlu_obj):
        """Predict Slot."""
        tokens = nlu_obj['tokens']
        ret = self.predict([tokens])
        ner_ret = get_slots_detail(tokens, ret[0][-len(tokens):])
        nlu_obj['ner_slot_filler'] = {'slots': ner_ret}
        for slot in ner_ret:
            slot['from'] = 'ner_slot_filler'
        if len(nlu_obj['slots']) <= 0:
            nlu_obj['slots'] = ner_ret
        else:
            for slot in ner_ret:
                is_include = False
                for s in nlu_obj['slots']:
                    if slot['pos'][0] >= s['pos'][0] and slot['pos'][0] <= s[
                            'pos'][1]:
                        is_include = True
                        break
                    elif slot['pos'][1] >= s['pos'][0] and slot['pos'][1] <= s[
                            'pos'][1]:
                        is_include = True
                        break
                    elif s['pos'][0] >= slot['pos'][0] and s['pos'][0] <= slot[
                            'pos'][1]:
                        is_include = True
                        break
                    elif s['pos'][1] >= slot['pos'][0] and s['pos'][1] <= slot[
                            'pos'][1]:
                        is_include = True
                        break
                if not is_include:
                    nlu_obj['slots'].append(slot)
                    nlu_obj['slots'] = sorted(
                        nlu_obj['slots'], key=lambda x: x['pos'][0])

        return nlu_obj

    def predict(self, sentence_result):
        """Predict sentence."""
        assert self.ner is not None, 'model not fitted'
        # import pdb; pdb.set_trace()
        seq = self.tokenizer.texts_to_sequences(sentence_result)
        seq_pad = pad_sequences(seq, maxlen=self.maxlen)
        y_pred = self.ner.predict_proba(seq_pad)
        y_pred = y_pred.argmax(-1)
        y_pred = self.tokenizer_y.sequences_to_texts(y_pred)
        y_pred = tuple([
            y.split(' ')[-len(s):]
            for s, y in zip(sentence_result, y_pred)
        ])
        return y_pred

    def eval(self, sentence_result, slot_result):
        """Evaluate."""
        y_pred = self.predict(sentence_result)
        y_test = slot_result
        acc = 0
        bad = []
        for sent, real, pred in zip(sentence_result, y_test, y_pred):
            real_slot = get_slots(sent, real)
            pred_slot = get_slots(sent, pred)
            a = get_exact_right(real_slot, pred_slot)
            acc += a
            if not a:
                bad.append((sent, real, pred, real_slot, pred_slot))
        acc /= len(sentence_result)
        return acc, bad
