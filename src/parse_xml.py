import os
from pathlib import Path

DATA_DIR = "data/"


def split_xml_files() -> None:
    target_dir = DATA_DIR + "split/"

    Path(target_dir).mkdir(parents=True, exist_ok=True)

    for filename in os.listdir(DATA_DIR):
        if filename.lower().endswith(".xml"):
            filename = filename.replace(".xml", "")
            filename = filename.replace(".XML", "")

            old_file = open(DATA_DIR + filename + ".xml", "r", encoding="iso-8859-1")

            dataset_number = 1
            for line in old_file:
                new_file = open(target_dir + filename + "_" + str(dataset_number) + ".xml", "w", encoding="iso-8859-1")
                new_file.write(line)
                new_file.close()
                dataset_number += 1

            old_file.close()
