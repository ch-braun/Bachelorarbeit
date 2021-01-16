from datetime import datetime
import os
from pathlib import Path
import re
import xml.etree.ElementTree as elemTree

# Dateipfade
DATA_DIR = "data/"
SPLIT_DIR = DATA_DIR + "split/"
STAT_DIR = DATA_DIR + "stat/"

# Globale Speicher


def split_xml_files(overwrite=False) -> None:
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
                    if overwrite or not os.path.exists(SPLIT_DIR + filename + "_" + str(dataset_number) + ".xml"):
                        new_file = open(SPLIT_DIR + filename + "_" + str(dataset_number) + ".xml", "w", encoding="iso-8859-1")
                        new_file.write(line)
                        new_file.close()
                        print("Wrote file: ", filename + "_" + str(dataset_number) + ".xml")
                        dataset_number += 1

            old_file.close()


def parse_xml_file(filename) -> elemTree.Element:
    tree = elemTree.parse(filename)
    return tree.getroot()


def create_table_stats() -> None:
    print("Creating table statistics...")
    tables = dict()
    table_stat_file = "table_stat_" + datetime.now().strftime("%Y-%m-%d (%H:%M:%S)") + ".csv"
    for filename in os.listdir(SPLIT_DIR):
        if filename.lower().endswith(".xml"):
            root = parse_xml_file(SPLIT_DIR + filename)
            heap = None
            file_tables = dict()

            print("Processing ", filename)

            for elem in root:
                elem.tag = re.sub(r'{.*}', '', elem.tag.lower())
                if elem.tag == 'heap':
                    heap = elem
                    break

            if heap is not None:
                for elem in heap:
                    elem.tag = re.sub(r'{.*}', '', elem.tag.lower())

                    if elem.tag.lower() not in file_tables.keys():
                        file_tables[elem.tag.lower()] = 1
                        if elem.tag.lower() in tables.keys():
                            tables[elem.tag.lower()] += 1
                        else:
                            tables[elem.tag.lower()] = 1

    header = ';'.join(map(str, tables.keys()))
    content = ';'.join(map(str, tables.values()))
    table_stat_file = open(STAT_DIR + table_stat_file, "w", encoding="utf-8")
    table_stat_file.write(header + "\n")
    table_stat_file.write(content + "\n")
    table_stat_file.close()


def create_score_stats() -> None:
    print("Creating score statistics...")
    score_stats = list()
    score_stat_file = "score_stat_" + datetime.now().strftime("%Y-%m-%d (%H:%M:%S)") + ".csv"
    file_scores = {"file_name": "", "1": 0, "2": 0, "3": 0, "4": 0,
                   "5": 0, "6": 0, "7": 0, "8": 0, "9": 0, "10": 0, "11": 0, "12": 0, "99": 0}
    counter = 0
    for filename in os.listdir(SPLIT_DIR):
        if filename.lower().endswith(".xml"):
            root = parse_xml_file(SPLIT_DIR + filename)
            heap = None
            file_scores = {"file_name": filename, "1": 0, "2": 0, "3": 0, "4": 0,
                           "5": 0, "6": 0, "7": 0, "8": 0, "9": 0, "10": 0, "11": 0, "12": 0, "99": 0}
            counter += 1
            print(counter, "Processing", filename)

            for elem in root:
                elem.tag = re.sub(r'{.*}', '', elem.tag.lower())
                if elem.tag == 'heap':
                    heap = elem
                    break

            if heap is not None:
                for elem in heap:
                    elem.tag = re.sub(r'{.*}', '', elem.tag.lower())

                    if elem.tag.lower() == "zdkk_rb_scores":
                        for column in elem:
                            column.tag = re.sub(r'{.*}', '', column.tag.lower())

                            if column.tag == "score1":
                                file_scores[str(column.text)] += 1
                                break

            score_stats.append(file_scores)

    score_stat_file = open(STAT_DIR + score_stat_file, "w", encoding="utf-8")
    header = ";".join(file_scores.keys())
    score_stat_file.write(header + "\n")

    for line in score_stats:
        line = ";".join(str(x) for x in line.values())
        score_stat_file.write(line + "\n")

    score_stat_file.close()


# split_xml_files()
# create_table_stats()
create_score_stats()
