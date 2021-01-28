import argparse
import shutil
from datetime import datetime
import os
import re
import xml.etree.ElementTree as elemTree
from pathlib import Path

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


def preprocess_entities(no_save: bool) -> None:
    timestamp = datetime.now().strftime("%Y_%m_%d_(%H-%M-%S)")
    current_output_dir = FLATTENED_DIR + timestamp + "/"
    if not no_save:    
        Path(current_output_dir).mkdir(parents=True, exist_ok=True)

    flattened_entities = dict()

    print("Preprocessing entities...")
    counter = 0
    for filename in os.listdir(SPLIT_DIR):
        if filename.lower().endswith(".xml"):
            heap = xml_tools.get_heap_node(SPLIT_DIR + filename)

            flattened = flatten_entity(heap)
            entity_name = re.sub(r'score.*cb', '', filename.lower()).replace('.xml', '')
            if not no_save:
                save_entity_to_file(entity=flattened, output_dir=current_output_dir, entity_name=entity_name)
            else:
                flattened_entities[entity_name] = flattened

            counter += 1
            breite = 0
            for key in flattened.keys():
                breite += len(flattened[key].keys())

            print(counter, filename, "preprocessed", breite)

    print(flattened_entities)


def do_step(args: argparse.Namespace) -> None:
    if args.clear_flattened:
        shutil.rmtree(FLATTENED_DIR)

    preprocess_entities(args.no_save)
