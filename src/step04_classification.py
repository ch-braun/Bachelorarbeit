import argparse
import os
import random
from datetime import datetime
from pathlib import Path

import numpy as np
from matplotlib import pyplot
from plot_keras_history import plot_history
from tensorflow import metrics
from tensorflow.keras import layers
from tensorflow.python.keras import Model, activations
from tensorflow.python.keras.backend import clear_session
from tensorflow.python.keras.utils.np_utils import to_categorical
from tensorflow.python.keras.utils.vis_utils import plot_model

from step01_data_collection import STAT_DIR, DATA_DIR
from step03_data_preprocessing import INDEPENDENT_DIR, NORMED_DIR

MODEL_DIR = DATA_DIR + "models/"

DATA = list()
LABELS = list()

TRAINING_DATA = list()
TRAINING_LABELS = list()

VALIDATION_DATA = list()
VALIDATION_LABELS = list()

SAMPLE = None
EPOCHS = 1
USE_NORMED = False


def divide_chunks(lst: list, n: int):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def load_data(use_normed=False):
    if use_normed:
        directory = NORMED_DIR
    else:
        directory = INDEPENDENT_DIR

    if len(os.listdir(directory)) == 0:
        return

    path = directory + max(os.listdir(directory)) + "/"
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


def split_data(target_sampling_amount=None):
    counts = dict()
    validation_counts = dict()
    sampling_factors = dict()
    sampling_counts = dict()
    for i in range(0, len(globals()['LABELS'])):
        label = str(globals()['LABELS'][i])
        if label in counts.keys():
            counts[label] += 1
        else:
            counts[label] = 1
            sampling_factors[label] = 1.0
            sampling_counts[label] = 0

    for key in counts.keys():
        validation_counts[key] = counts[key] // 10

    if target_sampling_amount is not None:
        for key in sampling_factors.keys():
            sampling_factors[key] = target_sampling_amount / counts[key]
            print(key, sampling_factors[key])

    for i in range(0, len(globals()['LABELS'])):
        label = str(globals()['LABELS'][i])
        entity = globals()['DATA'][i]

        if validation_counts[label] > 0:
            globals()['VALIDATION_DATA'].append(entity)
            globals()['VALIDATION_LABELS'].append(label)
            validation_counts[label] -= 1
        else:
            if int(sampling_factors[label]) >= 1:
                for x in range(0, int(sampling_factors[label])):
                    globals()['TRAINING_DATA'].append(entity)
                    globals()['TRAINING_LABELS'].append(label)
            else:
                mod = int(round(pow(sampling_factors[label], -1.0), 0))
                sampling_counts[label] %= mod
                if sampling_counts[label] == 0:
                    globals()['TRAINING_DATA'].append(entity)
                    globals()['TRAINING_LABELS'].append(label)

                sampling_counts[label] += 1

    globals()['TRAINING_DATA'] = np.asarray(globals()['TRAINING_DATA'])
    globals()['TRAINING_LABELS'] = np.asarray(globals()['TRAINING_LABELS'])
    globals()['VALIDATION_DATA'] = np.asarray(globals()['VALIDATION_DATA'])
    globals()['VALIDATION_LABELS'] = np.asarray(globals()['VALIDATION_LABELS'])

    print(1, len(list(filter(lambda l: l == '1', globals()['TRAINING_LABELS']))))
    print(2, len(list(filter(lambda l: l == '2', globals()['TRAINING_LABELS']))))
    print(4, len(list(filter(lambda l: l == '4', globals()['TRAINING_LABELS']))))
    print(6, len(list(filter(lambda l: l == '6', globals()['TRAINING_LABELS']))))
    print(7, len(list(filter(lambda l: l == '7', globals()['TRAINING_LABELS']))))
    print(8, len(list(filter(lambda l: l == '8', globals()['TRAINING_LABELS']))))
    print(9, len(list(filter(lambda l: l == '9', globals()['TRAINING_LABELS']))))

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
    if globals()['USE_NORMED']:
        inputs = layers.Input(shape=654)
    else:
        inputs = layers.Input(shape=77)
    hidden = layers.Dense(units=hidden_neurons, activation=activations.sigmoid, use_bias=True)(inputs)
    output = layers.Dense(10, use_bias=True, activation="softmax")(hidden)
    model = Model(inputs=inputs, outputs=output)

    model.summary()

    return model


def train_model(model: Model, epochs: int) -> dict:
    model.compile(optimizer='adam',
                  loss='mean_squared_error',
                  metrics=[metrics.CategoricalAccuracy(), metrics.Recall(), metrics.Precision()])

    y_train = to_categorical(globals()['TRAINING_LABELS'])
    y_validate = to_categorical(globals()['VALIDATION_LABELS'])
    print(y_train.shape)

    history = model.fit(x=globals()['TRAINING_DATA'], y=y_train, batch_size=32, epochs=epochs,
                        validation_data=(globals()['VALIDATION_DATA'], y_validate),
                        validation_batch_size=32,
                        validation_freq=1)

    return history.history


def validate_model(model: Model) -> [float, float, float, float]:
    y_validate = to_categorical(globals()['VALIDATION_LABELS'])
    print(y_validate.shape)

    loss, acc, recall, precision = model.evaluate(x=globals()['VALIDATION_DATA'], y=y_validate, batch_size=32)

    print("loss: %.4f" % loss)
    print("categorical accuracy: %.4f" % acc)
    print("recall: %.4f" % recall)
    print("precision: %.4f" % precision)

    return [loss, acc, recall, precision]


def validate_model_for_all_classes(model: Model) -> dict:
    class_labels = dict()
    class_entities = dict()
    results = dict()
    for i in range(0, len(globals()['VALIDATION_LABELS'])):
        if globals()['VALIDATION_LABELS'][i] not in class_labels.keys():
            class_labels[globals()['VALIDATION_LABELS'][i]] = list()
            class_entities[globals()['VALIDATION_LABELS'][i]] = list()
        class_labels[globals()['VALIDATION_LABELS'][i]].append(globals()['VALIDATION_LABELS'][i])
        class_entities[globals()['VALIDATION_LABELS'][i]].append(globals()['VALIDATION_DATA'][i])

    for key in class_labels.keys():
        label = np.asarray(class_labels[key] + ['9'])
        entities = np.asarray(class_entities[key])

        y_validate = to_categorical(label)[:-1]
        print(y_validate.shape)

        loss, acc, recall, precision = model.evaluate(x=entities, y=y_validate, batch_size=32)
        results[key] = [loss, acc, recall, precision]

    return results


def calculate_models(epochs=1, neurons=None):
    Path(STAT_DIR).mkdir(parents=True, exist_ok=True)
    Path(MODEL_DIR).mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y_%m_%d_(%H-%M-%S)")
    name_modifier = '_sample_' + str(SAMPLE) if SAMPLE is not None else '_sample_None'
    name_modifier += '_epochs' + str(EPOCHS)

    if globals()['USE_NORMED']:
        name_modifier = '_normed_' + name_modifier

    model_folder = MODEL_DIR + timestamp + name_modifier + '/'
    Path(model_folder).mkdir(parents=True, exist_ok=True)

    results = list()
    rare_results = list()
    if neurons is None:
        min_value = to_categorical(globals()['VALIDATION_LABELS']).shape[1]
        max_value = len(globals()['DATA'][0])+1
    else:
        min_value = neurons
        max_value = neurons + 1

    for x in range(min_value, max_value):
        print("Training NN for " + str(x) + " hidden neurons...")
        clear_session()
        model = create_neural_network(x)
        history = train_model(model, epochs)
        model.save(model_folder + "model_" + str(x))

        plot_history(history, path=model_folder + "model_" + str(x) + "/history.png", graphs_per_row=2)
        pyplot.close()

        plot_model(
            model,
            to_file=model_folder + "model_" + str(x) + "/model.png",
            show_shapes=True,
            show_layer_names=True,
            rankdir="TB",
            expand_nested=True,
            dpi=100,
        )

        results.append([x] + validate_model(model))
        temp = validate_model_for_all_classes(model)
        to_append = [x]
        for key in sorted(temp.keys()):
            to_append += temp[key]
        rare_results.append(to_append)

    output_file = model_folder + "models" + name_modifier + "_" + timestamp + '.csv'
    output_file = open(output_file, "w", encoding="utf-8")
    output_file.write('neurons;loss;accuracy;recall;precision\n')
    for r in results:
        output_file.write(";".join(list(map(str, r))) + "\n")
    output_file.close()

    rare_output_file = model_folder + "models" + name_modifier + "_rare_" + timestamp + '.csv'
    rare_output_file = open(rare_output_file, "w", encoding="utf-8")
    rare_output_file.write('neurons;loss 1;accuracy 1;recall 1;precision 1;loss 2;accuracy 2;recall 2;precision 2;' +
                           'loss 4;accuracy 4;recall 4;precision 4;' +
                           'loss 6;accuracy 6;recall 6;precision 6;loss 7;accuracy 7;recall 7;precision 7;' +
                           'loss 8;accuracy 8;recall 8;precision 8;loss 9;accuracy 9;recall 9;precision 9\n')
    for r in rare_results:
        rare_output_file.write(";".join(list(map(str, r))) + "\n")
    rare_output_file.close()


# 42 Neuronen im Hidden Layer
def do_step(args: argparse.Namespace) -> None:
    if not args.skip_classification:

        if not args.epochs:
            args.epochs = 1

        if not args.neurons:
            args.neurons = None

        globals()['EPOCHS'] = args.epochs
        globals()['NEURONS'] = args.neurons
        globals()['USE_NORMED'] = args.use_normed

        load_data(args.use_normed)
        if args.target_sampling_amount:
            globals()['SAMPLE'] = args.target_sampling_amount
            split_data(args.target_sampling_amount)
        else:
            split_data()

        calculate_models(epochs=args.epochs, neurons=args.neurons)
