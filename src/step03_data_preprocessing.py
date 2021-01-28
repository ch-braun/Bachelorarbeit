import argparse
import shutil
from datetime import datetime
import os
import re
import xml.etree.ElementTree as elemTree
from pathlib import Path
from filelock import FileLock

from step01_data_collection import DATA_DIR, SPLIT_DIR
from util import transformator
from util import xml_tools

FLATTENED_DIR = DATA_DIR + "flattened/"


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


def preprocess_entities(process_count: int) -> None:
    timestamp = datetime.now().strftime("%Y_%m_%d_(%H-%M-%S)")
    current_file_output_dir = FLATTENED_DIR + timestamp + "/"
    current_value_output_dir = current_file_output_dir + "values/"
    Path(current_file_output_dir).mkdir(parents=True, exist_ok=True)
    Path(current_value_output_dir).mkdir(parents=True, exist_ok=True)

    readers = list()
    print("Preprocessing entities...")
    files = list(filter(lambda f: f.lower().endswith(".xml"), os.listdir(SPLIT_DIR)))
    chunks = list(divide_chunks(files, len(files)//process_count))

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

            os.write(writer, bytearray('chunk preprocessed', "utf-8"))
            exit(0)

    for r in readers:
        print(os.read(r, 1000).decode())

    for filename in list(filter(lambda f: f.endswith('.lock'), os.listdir(current_value_output_dir))):
        try:
            os.remove(filename)
        except FileNotFoundError:
            continue


def do_step(args: argparse.Namespace) -> None:
    if args.clear_flattened:
        shutil.rmtree(FLATTENED_DIR, ignore_errors=True)

    if args.process_count is None or args.process_count == 0:
        args.process_count = 1

    preprocess_entities(args.process_count)
