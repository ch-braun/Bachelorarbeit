import os
from pathlib import Path
import xml.etree.ElementTree as et

DATA_DIR = "data/"
SPLIT_DIR = DATA_DIR + "split/"


def split_xml_files() -> None:
    Path(SPLIT_DIR).mkdir(parents=True, exist_ok=True)

    for filename in os.listdir(DATA_DIR):
        if filename.lower().endswith(".xml"):
            filename = filename.replace(".xml", "")
            filename = filename.replace(".XML", "")

            old_file = open(DATA_DIR + filename + ".xml", "r", encoding="iso-8859-1")

            dataset_number = 1
            for line in old_file:
                new_file = open(SPLIT_DIR + filename + "_" + str(dataset_number) + ".xml", "w", encoding="iso-8859-1")
                new_file.write(line)
                new_file.close()
                dataset_number += 1

            old_file.close()


def parse_xml_files() -> None:
    for filename in os.listdir(SPLIT_DIR):
        if filename.lower().endswith(".xml"):
            tree = et.parse(SPLIT_DIR + filename)
            root = tree.getroot()
            for child in root.iter("V_PARTNER"):
                print(filename, "|", child.tag, child.text)
                break

            for child in root.iter("SCORE1"):
                print(filename, "|", child.tag, child.text)


split_xml_files()
parse_xml_files()
