# -*- coding: utf-8 -*-
"""DST Module."""

from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.layers import LSTM
from keras.wrappers.scikit_learn import KerasClassifier


def make_model(n_size, n_output):
    """Create a Keras model."""
    model = Sequential()
    model.add(LSTM(n_size))
    model.add(Dense(n_output))
    model.add(Activation('sigmoid'))
    model.compile(loss='binary_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])

    return model


def get_model(n_output, n_size=64, epochs=5, batch_size=32):
    """Return Keras Model."""
    return KerasClassifier(
        make_model,
        batch_size=batch_size,
        n_output=n_output,
        epochs=epochs,
        n_size=n_size
    )
