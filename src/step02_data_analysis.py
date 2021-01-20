import argparse
from datetime import datetime
import os
import re
from pathlib import Path

from step01_data_collection import SPLIT_DIR, STAT_DIR
from util import xml_tools

DETAILED_STAT_DIR = STAT_DIR + "detailed/"


def create_stats() -> None:
    Path(STAT_DIR).mkdir(parents=True, exist_ok=True)
    Path(DETAILED_STAT_DIR).mkdir(parents=True, exist_ok=True)

    global_score_stats = list()
    global_table_stats = dict()

    file_score_stats = {"file_name": "", "1": 0, "2": 0, "3": 0, "4": 0, "5": 0,
                        "6": 0, "7": 0, "8": 0, "9": 0, "10": 0, "11": 0, "12": 0, "99": 0}

    score_stat_file = "score_stat_" + datetime.now().strftime("%Y_%m_%d_(%H-%M-%S)") + ".csv"
    table_stat_file = "table_stat_" + datetime.now().strftime("%Y_%m_%d_(%H-%M-%S)") + ".csv"

    print("Creating statistics...")
    counter = 0
    for filename in os.listdir(SPLIT_DIR):
        if filename.lower().endswith(".xml"):
            counter += 1
            file_score_stats = {"file_name": filename, "1": 0, "2": 0, "3": 0, "4": 0, "5": 0,
                                "6": 0, "7": 0, "8": 0, "9": 0, "10": 0, "11": 0, "12": 0, "99": 0}
            file_table_stats = dict()

            heap = xml_tools.get_heap_node(SPLIT_DIR + filename)

            if heap is not None:
                table_rows = xml_tools.get_table_rows_from_heap(heap)

                for row in table_rows:
                    # Create table statistics
                    if row.tag not in file_table_stats.keys():
                        file_table_stats[row.tag] = 1
                        if row.tag in global_table_stats.keys():
                            global_table_stats[row.tag] += 1
                        else:
                            global_table_stats[row.tag] = 1

                    # Create score statistics
                    if row.tag == 'zdkk_rb_scores':
                        file_score_stats[str(row.find('score1').text)] += 1

                global_score_stats.append(file_score_stats)
                print(counter, filename, "processed.")
            else:
                print(counter, filename, "has no heap.")

    header = ';'.join(map(str, global_table_stats.keys()))
    content = ';'.join(map(str, global_table_stats.values()))
    table_stat_file = open(STAT_DIR + table_stat_file, "w", encoding="utf-8")
    table_stat_file.write(header + "\n")
    table_stat_file.write(content + "\n")
    table_stat_file.close()

    score_stat_file = open(STAT_DIR + score_stat_file, "w", encoding="utf-8")
    header = ";".join(file_score_stats.keys())
    score_stat_file.write(header + "\n")

    for line in global_score_stats:
        line = ";".join(str(x) for x in line.values())
        score_stat_file.write(line + "\n")

    score_stat_file.close()


def do_step(args: argparse.Namespace) -> None:
    if not args.skip_stats:
        create_stats()
