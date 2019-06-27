# -*- coding: utf-8 -*-
"""NLU NER(Slot Filler) Module."""

from keras.models import Sequential
from keras.layers import Embedding, TimeDistributed, Dense

from keras_contrib.layers import CRF
from keras_contrib.losses import crf_loss
from keras_contrib.metrics import crf_viterbi_accuracy
from keras.layers import LSTM, Bidirectional, Activation
from keras.wrappers.scikit_learn import KerasClassifier


def make_model_crf(n_size, n_output, n_embedding, n_vocab):
    """Create Keras NER model."""
    model = Sequential()
    model.add(Embedding(n_vocab, n_embedding, mask_zero=True))
    model.add(Bidirectional(LSTM(n_size, return_sequences=True)))
    crf = CRF(n_output, sparse_target=True)
    model.add(crf)
    model.compile(
        optimizer='adam',
        loss=crf_loss,
        metrics=[crf_viterbi_accuracy])
    return model


def make_model(n_size, n_output, n_embedding, n_vocab):
    """Create Keras NER model."""
    model = Sequential()
    model.add(Embedding(n_vocab, n_embedding, mask_zero=True))
    model.add(Bidirectional(LSTM(n_size, return_sequences=True)))
    model.add(LSTM(n_size, return_sequences=True))
    model.add(TimeDistributed(Dense(n_output)))
    model.add(Activation('softmax'))
    model.compile(optimizer='adam', loss='categorical_crossentropy')
    return model


def get_model(n_output,
              n_size=100,
              batch_size=32,
              n_embedding=200,
              n_vocab=10000):
    """Return a Keras model."""
    clf = KerasClassifier(
        make_model,
        batch_size=batch_size,
        n_output=n_output,
        n_size=n_size,
        n_embedding=n_embedding,
        n_vocab=n_vocab
    )
    # Trick
    # KerasClassifier 只能接受 2-dim 的 y
    # 但是我们需要 3-dim 的 y
    setattr(
        clf,
        'model',
        make_model(n_size, n_output, n_embedding, n_vocab))
    return clf
