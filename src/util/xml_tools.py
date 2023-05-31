import re
import xml.etree.ElementTree as elemTree

from typing import List


def get_heap_node(filename) -> elemTree.Element:
    root = elemTree.parse(filename).getroot()

    for elem in root.iter():
        elem.tag = re.sub(r'{.*}', '', elem.tag.lower())

    return root.find('heap')


def get_table_rows_from_heap(heap: elemTree.Element) -> List[elemTree.Element]:
    tables = list()

    for table in heap:
        tables.append(table)

    return tables
