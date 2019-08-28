import os
import sys
import re
import stackoverflow as stackapi
from bs4 import BeautifulSoup
from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, ID
from whoosh.qparser import QueryParser
from whoosh import scoring
from whoosh.index import open_dir

ADDITION_SEARCH = 3


def processText(body):
    soup = BeautifulSoup(body, features="html.parser")
    text = soup.text
    tags = ["<strong>", "</strong>", "<code>", "</code>", "<em>", "</em>", "\n", "<p>",
            "</p>", "'", '"', "</a>", "\n", "\\'", "\'", "<pre>", "</pre>", "\\\\", "\\", "\\n","?"]
    for tag in tags:
        text = text.replace(tag, "")
    return text.lower()


def extract_stack_code(url):
    # identify the stackcode from the url
    regex_syntax = "https://stackoverflow\.com/questions/" + \
        r'([0-9]+)' + r'/.+'
    re_string = re.compile(regex_syntax)
    code = re.findall(re_string, url)
    return code[0] if len(code) == 1 else None


def get_search_index(query, topN=5):
    ix = open_dir("indexdir")
    searcher = ix.searcher(weighting=scoring.BM25F)
    query = QueryParser("content", ix.schema).parse(query)
    results = searcher.search(query, limit=topN)
    lists = [x['path'] for x in results]
    lists = [extract_stack_code(url) for url in lists]
    return lists


def createSearchableData(web_docs):
    schema = Schema(title=TEXT(stored=True), path=ID(stored=True),
                    content=TEXT, textdata=TEXT(stored=True))
    if not os.path.exists("indexdir"):
        os.mkdir("indexdir")

    ix = create_in("indexdir", schema)
    writer = ix.writer()

    for doc in web_docs:
        text = doc['text']
        title = doc['title']
        writer.add_document(title=title, path=doc['url'],
                            content=text, textdata=text)
    writer.commit()


def get_all_question_and_answers(text, num_results=5):
    query = processText(text)
    question_codes = get_search_index(query, num_results + ADDITION_SEARCH)
    question_codes = list(set(question_codes))[:num_results]
    print(question_codes)
    QnA_list = []
    for code in question_codes:
        item = stackapi.get_question_and_answers(code)

        if len(item['answers']) != 0:
            QnA_list.append(item)

    return QnA_list


if __name__ == "__main__":
    query = input("Enter query:")
    topN = 5
    print(get_search_index(query, topN))
