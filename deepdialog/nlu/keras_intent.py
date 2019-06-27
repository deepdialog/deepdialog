# -*- coding: utf-8 -*-
"""NLU Keras Module."""

from keras.models import Sequential
from keras.layers import Dense, Activation, Embedding
from keras.layers import LSTM
from keras.wrappers.scikit_learn import KerasClassifier


def make_model(n_size, n_output, n_embedding, n_vocab):
    """Create NLU Intent Keras Module."""
    model = Sequential()
    model.add(Embedding(n_vocab, n_embedding, mask_zero=True))
    model.add(LSTM(n_size))
    model.add(Dense(n_output))
    model.add(Activation('softmax'))
    model.compile(loss='categorical_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])
    return model


def get_model(n_output,
              n_size=64, epochs=10,
              batch_size=32,
              n_embedding=100,
              n_vocab=10000):
    """Return NLU Classifier."""
    return KerasClassifier(
        make_model,
        batch_size=batch_size,
        n_output=n_output,
        epochs=epochs,
        n_size=n_size,
        n_embedding=n_embedding,
        n_vocab=n_vocab
    )
