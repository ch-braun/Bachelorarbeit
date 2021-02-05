import argparse
import os
import random

import numpy as np
from tensorflow.keras import layers
from tensorflow.python.keras import Model, activations
from tensorflow.python.keras.utils.np_utils import to_categorical

from step03_data_preprocessing import INDEPENDENT_DIR

DATA = list()
LABELS = list()

TRAINING_DATA = list()
TRAINING_LABELS = list()

VALIDATION_DATA = list()
VALIDATION_LABELS = list()


def divide_chunks(lst: list, n: int):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def load_data():
    if len(os.listdir(INDEPENDENT_DIR)) == 0:
        return

    path = INDEPENDENT_DIR + max(os.listdir(INDEPENDENT_DIR)) + "/"
    files = list(filter(lambda f: f.lower().endswith('.csv'), os.listdir(path)))
    random.shuffle(files)

    print('Loading data from', path, '...')
    for filename in files:
        input_file = open(path + filename, "r")
        attributes = dict()
        for line in input_file:
            line = line.rstrip('\n')
            split = line.split(';')
            if len(split) == 2:
                attributes[split[0]] = float(split[1])

        input_file.close()

        temp = list()
        for key in sorted(attributes.keys()):
            temp.append(attributes[key])

        globals()['DATA'].append(temp)
        globals()['LABELS'].append(int(filename.split('_')[0]))

    globals()['DATA'] = np.asarray(globals()['DATA'])
    globals()['LABELS'] = np.asarray(globals()['LABELS'])

    print('Data shape:', globals()['DATA'].shape)
    print('Attribute data types:', globals()['DATA'].dtype)
    print('Label shape:', globals()['LABELS'].shape)
    print('Label data types:', globals()['LABELS'].dtype)


def split_data():
    counts = dict()
    for i in range(0, len(globals()['LABELS'])):
        label = str(globals()['LABELS'][i])
        if label in counts.keys():
            counts[label] += 1
        else:
            counts[label] = 1

    for key in counts.keys():
        counts[key] //= 10

    for i in range(0, len(globals()['LABELS'])):
        label_vect = {'1': 0, '2': 0, '4': 0, '6': 0, '7': 0, '8': 0, '9': 0}
        label = str(globals()['LABELS'][i])
        entity = globals()['DATA'][i]

        label_vect[label] = 1
        if counts[label] > 0:
            globals()['VALIDATION_DATA'].append(entity)
            globals()['VALIDATION_LABELS'].append(label)
            counts[label] -= 1
        else:
            globals()['TRAINING_DATA'].append(entity)
            globals()['TRAINING_LABELS'].append(label)

    globals()['TRAINING_DATA'] = np.asarray(globals()['TRAINING_DATA'])
    globals()['TRAINING_LABELS'] = np.asarray(globals()['TRAINING_LABELS'])
    globals()['VALIDATION_DATA'] = np.asarray(globals()['VALIDATION_DATA'])
    globals()['VALIDATION_LABELS'] = np.asarray(globals()['VALIDATION_LABELS'])

    print('Training Data shape:', globals()['TRAINING_DATA'].shape)
    print('Training Attribute data types:', globals()['TRAINING_DATA'].dtype)
    print('Training Label shape:', globals()['TRAINING_LABELS'].shape)
    print('Training Label data types:', globals()['TRAINING_LABELS'].dtype)

    print('Validation Data shape:', globals()['VALIDATION_DATA'].shape)
    print('Validation Attribute data types:', globals()['VALIDATION_DATA'].dtype)
    print('Validation Label shape:', globals()['VALIDATION_LABELS'].shape)
    print('Validation Label data types:', globals()['VALIDATION_LABELS'].dtype)


def create_neural_network(hidden_neurons: int) -> Model:
    if hidden_neurons < 1:
        hidden_neurons = 1

    inputs = layers.Input(shape=77)
    hidden = layers.Dense(units=hidden_neurons, activation=activations.sigmoid, use_bias=True)(inputs)
    output = layers.Dense(10, use_bias=True, activation="softmax")(hidden)
    model = Model(inputs=inputs, outputs=output)

    model.summary()

    return model


def train_model(model: Model):
    model.compile(optimizer='rmsprop',
                  loss='mean_squared_error')

    print(globals()['TRAINING_LABELS'][:100])
    y_train = to_categorical(globals()['TRAINING_LABELS']-1)
    print(y_train.shape)
    model.fit(globals()['TRAINING_DATA'], y_train, batch_size=32, epochs=10)


# 42 Neuronen im Hidden Layer
def do_step(args: argparse.Namespace) -> None:
    if not args.skip_classification:
        load_data()
        split_data()
        train_model(create_neural_network(42))

