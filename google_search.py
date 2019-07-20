import urllib
import requests
import json
from bs4 import BeautifulSoup
import re
import stackoverflow as stackapi
import pprint
'''
Custom Google Api to search for top k relevant questions from stackoverflow and get its code
K can be modified by chaning value in the num_results
'''

ADDITION_SEARCH = 3


def process_google_query(query):
    tags = ["'", '"', '|', '(', ')', '-', '~', '+']
    others = ['intitle:', 'allintitle:', 'inurl:', 'allinurl:',
              'intext:', 'allintext:', 'filetype:', 'related:']
    for tag in tags:
        query = query.replace(tag, '')
    for tag in others:
        query = query.replace(tag, '"'+tag+'"')
    return query


def extract_stack_code(url):
    # identify the stackcode from the url
    regex_syntax = "https://stackoverflow\.com/questions/" + \
        r'([0-9]+)' + r'/.+'
    re_string = re.compile(regex_syntax)
    code = re.findall(re_string, url)
    return code[0] if len(code) == 1 else None


def search_stackcodes(query, site=None, num_results=5):
    # identify all the stackcodes for the questions given in query
    query = process_google_query(query)
    url = "http://www.google.com/search?q="+query + \
        (" site:"+site if site is not None else "") + "&num="+str(num_results)
    stackcodes = []
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    urls = []
    for a in soup.find_all('a', href=True):
        tempUrl = a['href']
        urls.append(tempUrl)
        code = extract_stack_code(tempUrl)
        if code is not None:
            stackcodes.append(code)
    return stackcodes


def get_all_question_and_answers(text, num_results=5):

    question_codes = search_stackcodes(
        query=text, site='stackoverflow.com', num_results=num_results + ADDITION_SEARCH)
    question_codes = list(set(question_codes))[:num_results]
    QnA_list = []
    for code in question_codes:
        QnA_list.append(stackapi.get_question_and_answers(code))

    # QnA_list = sorted(
    #     QnA_list, key=lambda x: x['question']['score'], reverse=True)
    return QnA_list


if __name__ == "__main__":
    text = "how to run python"
    lists = get_all_question_and_answers(text)
    pprint.pprint(lists)
