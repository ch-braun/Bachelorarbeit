import argparse
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
            flattened = transform_func(grouped_rows[table_name])
        else:
            flattened = transform_func(list())

        if flattened is not None:
            flattened_entity[table_name] = flattened

    return flattened_entity


def preprocess_entities() -> None:
    Path(FLATTENED_DIR).mkdir(parents=True, exist_ok=True)

    flattened_entities = dict()
    print("Preprocessing entities...")
    counter = 0
    for filename in os.listdir(SPLIT_DIR):
        if filename.lower().endswith(".xml"):
            heap = xml_tools.get_heap_node(SPLIT_DIR + filename)

            flattened = flatten_entity(heap)
            entity_name = re.sub(r'score.*cb', '', filename.lower())
            flattened_entities[entity_name] = flattened

            counter += 1
            print(counter, filename, "preprocessed")

    print(flattened_entities)


def do_step(args: argparse.Namespace) -> None:
    preprocess_entities()
