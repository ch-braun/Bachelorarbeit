from datetime import datetime
import os
from pathlib import Path
import re
import xml.etree.ElementTree as elemTree

DATA_DIR = "data/"
SPLIT_DIR = DATA_DIR + "split/"
STAT_DIR = DATA_DIR + "stat/"


def split_xml_files() -> None:
    print("Splitting XML-files...")
    Path(SPLIT_DIR).mkdir(parents=True, exist_ok=True)
    Path(STAT_DIR).mkdir(parents=True, exist_ok=True)

    for filename in os.listdir(DATA_DIR):
        if filename.lower().endswith(".xml"):
            filename = filename.replace(".xml", "")
            filename = filename.replace(".XML", "")

            old_file = open(DATA_DIR + filename + ".xml", "r", encoding="iso-8859-1")

            dataset_number = 1
            for line in old_file:
                if line.startswith('<?xml version="1.0" encoding="iso-8859-1"?>'):
                    new_file = open(SPLIT_DIR + filename + "_" + str(dataset_number) + ".xml", "w", encoding="iso-8859-1")
                    new_file.write(line)
                    new_file.close()
                    print("Wrote file: ", filename + "_" + str(dataset_number) + ".xml")
                    dataset_number += 1

            old_file.close()


def parse_xml_file(filename) -> elemTree.Element:
    tree = elemTree.parse(filename)
    return tree.getroot()


def create_dataset_stats() -> None:
    print("Creating dataset statistics...")
    tables = dict()
    stat_file = "stat_" + datetime.now().strftime("%Y-%m-%d (%H:%M:%S)") + ".csv"
    for filename in os.listdir(SPLIT_DIR):
        if filename.lower().endswith(".xml"):
            root = parse_xml_file(SPLIT_DIR + filename)
            heap = None
            file_tables = dict()
            for elem in root:
                elem.tag = re.sub(r'{.*}', '', elem.tag.lower())
                if elem.tag == 'heap':
                    heap = elem
                    break

            if heap is not None:
                for elem in heap:
                    elem.tag = re.sub(r'{.*}', '', elem.tag.lower())
                    print(filename, elem.tag)
                    if elem.tag.lower() not in file_tables.keys():
                        file_tables[elem.tag.lower()] = 1
                        if elem.tag.lower() in tables.keys():
                            tables[elem.tag.lower()] += 1
                        else:
                            tables[elem.tag.lower()] = 1

    header = ';'.join(map(str, tables.keys()))
    content = ';'.join(map(str, tables.values()))
    stat_file = open(STAT_DIR + stat_file, "w", encoding="utf-8")
    stat_file.write(header + "\n")
    stat_file.write(content + "\n")
    stat_file.close()


split_xml_files()
create_dataset_stats()
