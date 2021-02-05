import argparse
import os
import random
from datetime import datetime
from pathlib import Path

import numpy as np
from tensorflow import metrics
from tensorflow.keras import layers
from tensorflow.python.keras import Model, activations
from tensorflow.python.keras.backend import clear_session
from tensorflow.python.keras.utils.np_utils import to_categorical

from step01_data_collection import STAT_DIR, DATA_DIR
from step03_data_preprocessing import INDEPENDENT_DIR

MODEL_DIR = DATA_DIR + "models/"

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
            if 1 < int(label) < 9:
                for x in range(0, 10):
                    globals()['VALIDATION_DATA'].append(entity)
                    globals()['VALIDATION_LABELS'].append(label)
            else:
                globals()['VALIDATION_DATA'].append(entity)
                globals()['VALIDATION_LABELS'].append(label)
            counts[label] -= 1
        else:
            if 1 < int(label) < 9:
                for x in range(0, 10):
                    globals()['TRAINING_DATA'].append(entity)
                    globals()['TRAINING_LABELS'].append(label)
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
                  loss='mean_squared_error',
                  metrics=[metrics.CategoricalAccuracy(), metrics.Recall(), metrics.Precision()])

    y_train = to_categorical(globals()['TRAINING_LABELS'])
    print(y_train.shape)

    history = model.fit(x=globals()['TRAINING_DATA'], y=y_train, batch_size=32, epochs=10)
    print(history.history)


def validate_model(model: Model) -> [float, float, float, float]:
    y_validate = to_categorical(globals()['VALIDATION_LABELS'])
    print(y_validate.shape)

    loss, acc, recall, precision = model.evaluate(x=globals()['VALIDATION_DATA'], y=y_validate, batch_size=32)

    print("loss: %.4f" % loss)
    print("categorical accuracy: %.4f" % acc)
    print("recall: %.4f" % recall)
    print("precision: %.4f" % precision)

    return [loss, acc, recall, precision]


def validate_model_for_rare_classes(model: Model) -> [float, float, float, float]:
    rare_labels = list()
    rare_entities = list()
    for i in range(0, len(globals()['VALIDATION_LABELS'])):
        if int(globals()['VALIDATION_LABELS'][i]) > 1:
            rare_labels.append(globals()['VALIDATION_LABELS'][i])
            rare_entities.append(globals()['VALIDATION_DATA'][i])

    rare_labels = np.asarray(rare_labels)
    rare_entities = np.asarray(rare_entities)

    y_validate = to_categorical(rare_labels)
    print(y_validate.shape)

    loss, acc, recall, precision = model.evaluate(x=rare_entities, y=y_validate, batch_size=32)

    print("loss: %.4f" % loss)
    print("categorical accuracy: %.4f" % acc)
    print("recall: %.4f" % recall)
    print("precision: %.4f" % precision)

    return [loss, acc, recall, precision]


def calculate_models():
    Path(STAT_DIR).mkdir(parents=True, exist_ok=True)
    Path(MODEL_DIR).mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y_%m_%d_(%H-%M-%S)")

    model_folder = MODEL_DIR + timestamp + '/'
    Path(model_folder).mkdir(parents=True, exist_ok=True)

    results = list()
    rare_results = list()
    min_value = to_categorical(globals()['VALIDATION_LABELS']).shape[1]
    max_value = len(globals()['DATA'][0])+1
    max_value = 20

    for x in range(min_value, max_value):
        print("Training NN for " + str(x) + " hidden neurons...")
        clear_session()
        model = create_neural_network(x)
        train_model(model)
        model.save(model_folder + "model_" + str(x))
        results.append([x] + validate_model(model))
        rare_results.append([x] + validate_model_for_rare_classes(model))

    output_file = STAT_DIR + "models_" + timestamp + '.csv'
    output_file = open(output_file, "w", encoding="utf-8")
    output_file.write('neurons;loss;accuracy;recall;precision\n')
    for r in results:
        output_file.write(";".join(list(map(str, r))) + "\n")
    output_file.close()

    rare_output_file = STAT_DIR + "models_rare_" + timestamp + '.csv'
    rare_output_file = open(rare_output_file, "w", encoding="utf-8")
    rare_output_file.write('neurons;loss;accuracy;recall;precision\n')
    for r in rare_results:
        rare_output_file.write(";".join(list(map(str, r))) + "\n")
    rare_output_file.close()


# 42 Neuronen im Hidden Layer
def do_step(args: argparse.Namespace) -> None:
    if not args.skip_classification:
        load_data()
        split_data()
        calculate_models()
