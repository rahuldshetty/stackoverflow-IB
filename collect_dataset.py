import requests
from stackoverflow2 import *
import re
import json
from indexer import *

page_begin = 1
COUNT = 100500  # change the parameter to limit the specify amount of


if __name__ == "__main__":
    get_questions_list(COUNT, page_begin)
    lists = json.load(open('data.json', 'r'))
    createSearchableData(lists)
