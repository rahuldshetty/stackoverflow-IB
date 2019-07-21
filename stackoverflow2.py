from stackapi import StackAPI
from bs4 import BeautifulSoup
import re
from indexer import *
import os
import json
import time

web = StackAPI('stackoverflow', key='DOn2V4wfc7dWSnCG9bzbSg((',)


# PARAMAETERS FOR SEARCH
SORT = "votes"  # "activity" "votes" "creation"
PAGESIZE = 100


def get_all_questions(page_no):
    return web.fetch('questions',  pagesize=PAGESIZE, page=page_no, filter="withbody", sort="votes", order="desc")['items']


def getQuestion(question):
    url = question['link']
    title = processText(question['title'])
    body = title + " " + processText(question['body'])
    return {
        'text': body,
        'title': title,
        'url': url
    }


def get_list_size():
    val = 0
    try:
        val = len(json.load(open('data.json', 'r')))
    except:
        val = 0
    return val


def get_questions_list(count, page_begin):
    timeout = 5
    while True and get_list_size() <= count:
        if timeout == 0:
            print('Error in api')
            break
        pages = get_all_questions(page_begin)
        print('Found', len(pages), 'items in page_no:', page_begin)
        print(pages[0]['title'])
        lists = [getQuestion(page) for page in pages]
        page_begin += 1
        if len(pages) == 0:
            timeout -= 1
        else:
            if os.path.exists('data.json'):
                file = open('data.json', 'r')
                laod_data = json.load(file)
                laod_data += lists
                file.close()
                file = open('data.json', 'w')
                json.dump(laod_data, file)
                file.close()
            else:
                file = open('data.json', 'w')
                json.dump(lists, file)
                file.close()
        print("LIST SIZE:", get_list_size())
        time.sleep(2)
