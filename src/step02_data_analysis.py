import argparse
import os
from datetime import datetime
from pathlib import Path

from step01_data_collection import SPLIT_DIR, STAT_DIR, DATA_DIR
from util import xml_tools

DETAILED_GLOBAL_STAT_DIR = STAT_DIR + "detailed_global/"
REQUESTED_COLUMNS_DIR = DATA_DIR + "requested_columns/"

COLUMN_VALUES = dict()


def create_stats() -> None:
    Path(STAT_DIR).mkdir(parents=True, exist_ok=True)
    Path(DETAILED_GLOBAL_STAT_DIR).mkdir(parents=True, exist_ok=True)
    Path(REQUESTED_COLUMNS_DIR).mkdir(parents=True, exist_ok=True)

    global_score_stats = list()
    global_table_stats = dict()
    global_column_stats = dict()

    file_score_stats = {"file_name": "", "1": 0, "2": 0, "3": 0, "4": 0, "5": 0,
                        "6": 0, "7": 0, "8": 0, "9": 0, "10": 0, "11": 0, "12": 0, "99": 0}

    ts = datetime.now().strftime("%Y_%m_%d_(%H-%M-%S)")
    score_stat_file = "score_stat_" + ts + ".csv"
    table_stat_file = "table_stat_" + ts + ".csv"
    column_stat_file = "_column_stat_" + ts + ".csv"
    column_values_file = "column_values_" + ts + ".csv"

    requested_columns = dict()
    if Path(REQUESTED_COLUMNS_DIR + 'columns.txt').exists():
        column_request_file = open(REQUESTED_COLUMNS_DIR + 'columns.txt', "r", encoding="iso-8859-1")
        check_values = True
        for line in column_request_file:
            line = line.replace("\n", '')
            line = line.split('->')
            if line[0] in requested_columns.keys():
                requested_columns[line[0]].append(line[1])
            else:
                requested_columns[line[0]] = [line[1]]
    else:
        check_values = False

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

                if check_values:
                    grouped_rows = dict()
                    for element in table_rows:
                        if element.tag not in grouped_rows.keys():
                            grouped_rows[element.tag] = list()

                        grouped_rows[element.tag].append(element)

                    get_values_of_specified_columns(requested_columns, grouped_rows)

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

                    # Create column statistics
                    if row.tag not in global_column_stats.keys():
                        global_column_stats[row.tag] = dict()

                    if 'total_rows' not in global_column_stats[row.tag].keys():
                        global_column_stats[row.tag]['total_rows'] = 1
                    else:
                        global_column_stats[row.tag]['total_rows'] += 1

                    for column in row:
                        if column.text is not None and column.text != '':
                            if column.tag not in global_column_stats[row.tag].keys():
                                global_column_stats[row.tag][column.tag] = 1
                            else:
                                global_column_stats[row.tag][column.tag] += 1

                global_score_stats.append(file_score_stats)
                print(counter, filename, "processed.")
            else:
                print(counter, filename, "has no heap.")

    # Save table statistics
    table_stat_file = open(STAT_DIR + table_stat_file, "w", encoding="utf-8")
    for key in global_table_stats.keys():
        table_stat_file.write(str(key) + ";" + str(global_table_stats[key]) + "\n")
    table_stat_file.close()

    # Save score statistics
    score_stat_file = open(STAT_DIR + score_stat_file, "w", encoding="utf-8")
    header = ";".join(map(str, file_score_stats.keys()))
    score_stat_file.write(header + "\n")
    for line in global_score_stats:
        line = ";".join(map(str, line.values()))
        score_stat_file.write(line + "\n")
    score_stat_file.close()

    # Save column statistics
    for key in global_column_stats.keys():
        file = open(DETAILED_GLOBAL_STAT_DIR + key + column_stat_file, "w", encoding="utf-8")
        for col_key in global_column_stats[key].keys():
            file.write(str(col_key) + ";" + str(global_column_stats[key][col_key]) + "\n")
        file.close()

    # Save column values
    if check_values:
        column_values_file = open(DETAILED_GLOBAL_STAT_DIR + column_values_file, "w", encoding="utf-8")

        for key in COLUMN_VALUES.keys():
            column_values_file.write(str(key) + ";" + ";".join(map(str, COLUMN_VALUES[key])) + "\n")
        column_values_file.close()


def get_values_of_specified_columns(requested_columns: dict, grouped_rows: dict) -> None:
    for key in requested_columns.keys():

        if key in grouped_rows.keys():
            for column in requested_columns[key]:
                for row in grouped_rows[key]:

                    found_value = row.find(column)
                    if found_value is not None:
                        if key + ';' + column in COLUMN_VALUES.keys():
                            if found_value.text not in COLUMN_VALUES[key + ';' + column]:
                                COLUMN_VALUES[key + ';' + column].append(found_value.text)
                        else:
                            COLUMN_VALUES[key + ';' + column] = [found_value.text]


def do_step(args: argparse.Namespace) -> None:
    if not args.skip_stats:
        create_stats()
