import urllib
import requests
import json
from bs4 import BeautifulSoup
import re

'''
Custom Google Api to search for top k relevant questions from stackoverflow and get its code
K can be modified by chaning value in the num_results
'''


def extract_stack_code(url):
    # identify the stackcode from the url
    regex_syntax = "https://stackoverflow\.com/questions/" + \
        r'([0-9]+)' + r'/.+'
    re_string = re.compile(regex_syntax)
    code = re.findall(re_string, url)
    return code[0] if len(code) == 1 else None


def search_stackcodes(query, site=None, num_results=7):
    # identify all the stackcodes for the questions given in query
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


if __name__ == "__main__":
    text = "how to run python"
    question_codes = search_stackcodes(text, "stackoverflow.com")
