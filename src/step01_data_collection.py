import argparse
import os
import shutil
from pathlib import Path

from util import xml_tools

# Dateipfade
DATA_DIR = "data/"
SPLIT_DIR = DATA_DIR + "split/"
AMBIGUOUS_DIR = SPLIT_DIR + "ambiguous/"
STAT_DIR = DATA_DIR + "stat/"


def split_xml_files(overwrite=False) -> None:
    print("Splitting XML-files...")
    Path(SPLIT_DIR).mkdir(parents=True, exist_ok=True)

    counter = 0
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
                        counter += 1
                        print(counter, filename + "_" + str(dataset_number) + ".xml", "written.")
                        dataset_number += 1

            old_file.close()


def clean_scores() -> None:
    Path(AMBIGUOUS_DIR).mkdir(parents=True, exist_ok=True)
    counter = 0
    counter_valid = 0
    counter_ambiguous = 0
    for filename in os.listdir(SPLIT_DIR):
        if filename.lower().endswith(".xml"):
            heap = xml_tools.get_heap_node(SPLIT_DIR + filename)
            counter += 1
            if heap is not None:
                table_rows = xml_tools.get_table_rows_from_heap(heap)
                filtered_rows = list()
                for row in table_rows:
                    if row.tag == 'zdkk_rb_scores':
                        if row.find('score1').text is not None and int(row.find('score1').text) < 10:
                            filtered_rows.append(row)

                print(counter, filename, len(filtered_rows))
                if len(filtered_rows) == 1:
                    counter_valid += 1
                else:
                    counter_ambiguous += 1
                    shutil.move(SPLIT_DIR + filename, AMBIGUOUS_DIR + filename)
            else:
                counter_ambiguous += 1
                shutil.move(SPLIT_DIR + filename, AMBIGUOUS_DIR + filename)
                print(counter, filename, 'has no heap.')

    print("Valid:", counter_valid)
    print("Ambiguous:", counter_ambiguous)


def do_step(args: argparse.Namespace) -> None:
    if not args.skip_split:
        split_xml_files(args.overwrite)

    if args.clean_scores:
        clean_scores()
