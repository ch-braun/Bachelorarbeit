import argparse
import math
import shutil
from datetime import datetime
import os
import re
import xml.etree.ElementTree as elemTree
from pathlib import Path
from filelock import FileLock

from step01_data_collection import DATA_DIR, SPLIT_DIR
from step02_data_analysis import STAT_DIR
from util import transformator
from util import xml_tools
import numpy as np

FLATTENED_DIR = DATA_DIR + "flattened/"
NORMED_DIR = DATA_DIR + "normed/"
INDEPENDENT_DIR = DATA_DIR + "independent/"
VAR = dict()
MIN = dict()
MAX = dict()


def flatten_entity(entity_heap: elemTree.Element) -> dict:
    grouped_rows = dict()
    flattened_entity = dict()
    for element in xml_tools.get_table_rows_from_heap(entity_heap):
        if element.tag not in grouped_rows.keys():
            grouped_rows[element.tag] = list()

        grouped_rows[element.tag].append(element)

    for table_name in transformator.get_relevant_table_names():
        transform_func = transformator.get_transform_func_for_table_rows(table_name=table_name)
        if table_name in grouped_rows.keys():
            if table_name != 'fkk_sec' and table_name != 'fkk_sec_c':
                flattened = transform_func(grouped_rows[table_name])
            elif table_name == 'fkk_sec':
                sek = grouped_rows['fkk_sec'] if 'fkk_sec' in grouped_rows.keys() else list()
                sek_c = grouped_rows['fkk_sec_c'] if 'fkk_sec_c' in grouped_rows.keys() else list()
                flattened = transform_func(sek, sek_c)
            else:
                flattened = dict()
        else:
            flattened = transform_func(list())

        if flattened is not None:
            flattened_entity[table_name] = flattened

    return flattened_entity


def save_entity_to_file(entity: dict, output_dir: str, entity_name: str) -> None:
    filename = output_dir + entity_name + '.csv'
    file = open(filename, "w", encoding="utf-8")
    for key_tab in sorted(entity.keys()):
        for key_attr in sorted(entity[key_tab].keys()):
            file.write(str(key_attr) + ';' + str(entity[key_tab][key_attr]) + '\n')

    file.close()


def save_values_to_files(entity: dict, value_output_dir: str) -> None:
    for key_tab in entity.keys():
        for key_attr in entity[key_tab].keys():
            filename = value_output_dir + key_attr + '.csv'
            lock_filename = value_output_dir + key_attr + '.csv.lock'

            lock = FileLock(lock_filename, timeout=10)
            lock.acquire()
            try:
                open(filename, "a", encoding="utf-8").write(str(entity[key_tab][key_attr]) + '\n')
            finally:
                lock.release()


def divide_chunks(lst: list, n: int):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def flatten_all_entities(process_count: int) -> None:
    timestamp = datetime.now().strftime("%Y_%m_%d_(%H-%M-%S)")
    current_file_output_dir = FLATTENED_DIR + timestamp + "/"
    current_value_output_dir = current_file_output_dir + "values/"
    Path(current_file_output_dir).mkdir(parents=True, exist_ok=True)
    Path(current_value_output_dir).mkdir(parents=True, exist_ok=True)

    readers = list()
    print("Flattening entities...")
    files = list(filter(lambda f: f.lower().endswith(".xml"), os.listdir(SPLIT_DIR)))
    chunks = list(divide_chunks(files, len(files) // process_count))

    print(len(chunks), 'chunks')
    for chunk in chunks:
        # Erzeugen einer Pipe zur Interprozesskommunikation
        reader, writer = os.pipe()

        print('Starting new chunk...')

        # Erzeugen des Subprozesses
        if os.fork():
            # Hier läuft der Hauptprozess weiter
            # Pipe-Endpunkt des neuen Subprozesses an Liste anhängen
            readers.append(reader)
        else:
            counter = 0
            for filename in chunk:
                heap = xml_tools.get_heap_node(SPLIT_DIR + filename)

                flattened = flatten_entity(heap)
                entity_name = re.sub(r'score.*cb', '', filename.lower()).replace('.xml', '')
                save_entity_to_file(entity=flattened, output_dir=current_file_output_dir, entity_name=entity_name)
                save_values_to_files(entity=flattened, value_output_dir=current_value_output_dir)

                breite = 0
                for key in flattened.keys():
                    breite += len(flattened[key].keys())
                counter += 1

            os.write(writer, bytearray('chunk flattened', "utf-8"))
            exit(0)

    for r in readers:
        print(os.read(r, 1000).decode())

    for filename in list(filter(lambda f: f.endswith('.lock'), os.listdir(current_value_output_dir))):
        try:
            os.remove(filename)
        except FileNotFoundError:
            continue


def calculate_variances_and_extrema():
    print('Calculating variances...')
    if len(os.listdir(FLATTENED_DIR)) == 0:
        return

    path = FLATTENED_DIR + max(os.listdir(FLATTENED_DIR)) + "/values/"

    print('Selecting', path)

    files = list(filter(lambda f: f.lower().endswith(".csv"), os.listdir(path)))
    variances = dict()
    minima = dict()
    maxima = dict()
    for filename in files:
        print('Calculating', filename.lower().replace('.csv', ''))
        file = open(path + filename, "r")
        values = np.asarray([abs(float(line.rstrip('\n'))) for line in file])
        if max(values) != 0 and max(values) != min(values):
            normed = (values - min(values)) / (max(values) - min(values))
        else:
            normed = values

        variances[filename.lower().replace('.csv', '')] = np.var(normed)
        minima[filename.lower().replace('.csv', '')] = min(values)
        maxima[filename.lower().replace('.csv', '')] = max(values)

    variances = {k: v for k, v in sorted(variances.items(), key=lambda item: item[1])}
    globals()['VAR'] = variances.copy()
    globals()['MIN'] = minima.copy()
    globals()['MAX'] = maxima.copy()

    for key in globals()['VAR']:
        print(key, globals()['VAR'][key])

    zero_var = list(filter(lambda v: v == 0.0, variances.values()))
    nonzero_var = list(filter(lambda v: v > 0.0, variances.values()))
    print('Attributes having exactly 0.0 variance:', len(zero_var))
    print('Attributes having more than 0.0 variance:', len(nonzero_var))


def normalize_entites(process_count: int):
    timestamp = datetime.now().strftime("%Y_%m_%d_(%H-%M-%S)")
    current_file_output_dir = NORMED_DIR + timestamp + "/"
    Path(current_file_output_dir).mkdir(parents=True, exist_ok=True)

    readers = list()
    print("Normalizing entities...")
    path = FLATTENED_DIR + max(os.listdir(FLATTENED_DIR)) + "/"
    files = list(filter(lambda f: f.lower().endswith(".csv"), os.listdir(path)))

    chunks = list(divide_chunks(files, len(files) // process_count))
    print(len(chunks), 'chunks')

    for chunk in chunks:
        # Erzeugen einer Pipe zur Interprozesskommunikation
        reader, writer = os.pipe()

        print('Starting new chunk...')

        # Erzeugen des Subprozesses
        if os.fork():
            # Hier läuft der Hauptprozess weiter
            # Pipe-Endpunkt des neuen Subprozesses an Liste anhängen
            readers.append(reader)
        else:
            for filename in chunk:
                file = open(path + filename, "r")
                new_file = open(current_file_output_dir + filename.lower(), "w", encoding="utf-8")
                for line in file:
                    line = line.rstrip('\n')
                    if line is not None and line != '':
                        split = line.split(';', 1)
                        if VAR[split[0]] != 0:
                            minimum = MIN[split[0]]
                            maximum = MAX[split[0]]
                            value = abs(float(split[1]))
                            if maximum != 0 and maximum != minimum:
                                normed = (value - minimum) / (maximum - minimum)
                            else:
                                normed = value
                            new_file.write(split[0] + ";" + str(normed) + "\n")
                file.close()
                new_file.close()

            os.write(writer, bytearray('chunk normalized', "utf-8"))
            exit(0)

    for r in readers:
        print(os.read(r, 1000).decode())


def write_buffer_to_file(filename: str, lines: list):
    lock_filename = filename + '.lock'

    lock = FileLock(lock_filename, timeout=10)
    lock.acquire()
    try:
        out = open(filename, "a", encoding="utf-8")
        for line in lines:
            out.write(line + '\n')
    finally:
        lock.release()


def check_stat_independence(process_count: int):
    entities = list()
    path = NORMED_DIR + max(os.listdir(NORMED_DIR)) + "/"
    files = list(filter(lambda f: f.lower().endswith(".csv"), os.listdir(path)))
    output_filename = STAT_DIR + "correlation_" + datetime.now().strftime("%Y_%m_%d_(%H-%M-%S)") + ".csv"

    print('Checking statistical independence for all attributes')

    for filename in files:
        file = open(path + filename, "r")
        new_entity = dict()
        for line in file:
            line = line.rstrip('\n').split(';', 1)
            new_entity[line[0]] = float(line[1])
        entities.append(new_entity)

    combinations = math.comb(len(entities[0].keys()), 2)
    print('Combinations to check for independence:', combinations)

    attributes = list(entities[0].keys()).copy()
    cross_table = list()
    done = list()
    for a in attributes:
        for b in attributes:
            if a != b and b not in done:
                cross_table.append([a, b])
        done.append(a)

    print('Cross Table size: ', len(cross_table))

    chunks = divide_chunks(cross_table, len(cross_table) // process_count)
    readers = list()
    for chunk in chunks:
        # Erzeugen einer Pipe zur Interprozesskommunikation
        reader, writer = os.pipe()

        print('Starting new chunk...')

        # Erzeugen des Subprozesses
        if os.fork():
            # Hier läuft der Hauptprozess weiter
            # Pipe-Endpunkt des neuen Subprozesses an Liste anhängen
            readers.append(reader)
        else:
            buffer_array = list()
            for pair in chunk:
                values_a = list(map(lambda e: e[pair[0]], entities))
                values_b = list(map(lambda e: e[pair[1]], entities))
                std_a = np.std(values_a)
                std_b = np.std(values_b)
                mean_a = np.mean(values_a)
                mean_b = np.mean(values_b)
                n = len(values_a)
                accumulated_sum = 0.0
                for i in range(0, n):
                    accumulated_sum += (values_a[i] - mean_a) * (values_b[i] - mean_b)

                corr_coeff = accumulated_sum / (n * std_a * std_b)

                buffer_array.append(pair[0] + ";" + pair[1] + ";" + str(corr_coeff))

                if len(buffer_array) > 100:
                    write_buffer_to_file(output_filename, buffer_array)
                    buffer_array = list()

            write_buffer_to_file(output_filename, buffer_array)
            os.write(writer, bytearray('chunk checked', "utf-8"))
            exit(0)

    for r in readers:
        print(os.read(r, 1000).decode())

    try:
        os.remove(output_filename + ".lock")
    except FileNotFoundError:
        pass


def eliminate_dependent_attributes(process_count: int, crit_val=0.01):
    # crit_val = 0.114 --> alpha = 0.01, n = infinite
    files = list(filter(lambda f: f.lower().startswith('correlation_'), os.listdir(STAT_DIR)))
    if len(files) == 0:
        return

    output_path = INDEPENDENT_DIR + datetime.now().strftime("%Y_%m_%d_(%H-%M-%S)") + "/"
    Path(output_path).mkdir(parents=True, exist_ok=True)

    file = open(STAT_DIR + max(files), "r")
    lines = list(map(lambda l: l.rstrip('\n').split(';'), file.readlines()))
    lines = [[line[0], line[1], round(float(line[2]), 8)] for line in lines]
    lines = sorted(lines, key=lambda l: float(l[2]), reverse=True)

    print('Perfectly positively correlated pairs:', len(list(filter(lambda l: l[2] == 1.0, lines))))
    print('Perfectly negatively correlated pairs:', len(list(filter(lambda l: l[2] == -1.0, lines))))
    print('Perfectly uncorrelated pairs:', len(list(filter(lambda l: l[2] == 0.0, lines))))
    print('Uncorrelated pairs by critical value of ' + str(crit_val) + ':',
          len(list(filter(lambda l: abs(l[2]) <= crit_val, lines))))
    print('Correlated pairs by critical value of ' + str(crit_val) + ':',
          len(list(filter(lambda l: abs(l[2]) > crit_val, lines))))

    attributes = list(map(lambda l: l[0], lines))
    attributes += list(map(lambda l: l[1], lines))
    attributes = list(dict.fromkeys(attributes))

    for a, b, value in lines:
        if abs(value) > crit_val:
            attributes = list(map(lambda l: l if l != b else a, attributes))

    attributes = list(dict.fromkeys(attributes))
    print('Uncorrelated attributes by critical value of ' + str(crit_val) + ':', len(attributes))

    files = list(filter(lambda f: f.lower().endswith('.csv'), os.listdir(NORMED_DIR + max(os.listdir(NORMED_DIR)))))
    chunks = divide_chunks(files, len(files) // process_count)
    readers = list()

    for chunk in chunks:
        # Erzeugen einer Pipe zur Interprozesskommunikation
        reader, writer = os.pipe()

        print('Starting new chunk...')

        # Erzeugen des Subprozesses
        if os.fork():
            # Hier läuft der Hauptprozess weiter
            # Pipe-Endpunkt des neuen Subprozesses an Liste anhängen
            readers.append(reader)
        else:
            for filename in chunk:
                input_file = open(NORMED_DIR + max(os.listdir(NORMED_DIR)) + "/" + filename, "r")
                output_file = open(output_path + filename, "w")

                for line in input_file:
                    line = line.rstrip('\n')
                    split = line.split(';')
                    if len(split) == 2:
                        if split[0] in attributes:
                            output_file.write(line + '\n')

                input_file.close()
                output_file.close()

            os.write(writer, bytearray('chunk reduced to indepent attributes', "utf-8"))
            exit(0)

    for r in readers:
        print(os.read(r, 1000).decode())


def do_step(args: argparse.Namespace) -> None:
    if args.clear_flattened:
        shutil.rmtree(FLATTENED_DIR, ignore_errors=True)

    if not args.skip_flattening:
        flatten_all_entities(args.process_count)

    if not args.skip_norm:
        calculate_variances_and_extrema()
        normalize_entites(args.process_count)

    if not args.skip_independence_check:
        check_stat_independence(args.process_count)

    if args.crit_val is not None and args.crit_val > 0:
        eliminate_dependent_attributes(process_count=args.process_count, crit_val=args.crit_val)
    else:
        eliminate_dependent_attributes(process_count=args.process_count)
