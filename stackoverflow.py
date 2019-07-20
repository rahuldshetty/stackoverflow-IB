import urllib
import requests
import json
from bs4 import BeautifulSoup
import re
import pprint

'''
Custom Stackoverflow API for getting user,question and answer details
'''


def process_date(date_string):
    if date_string is None:
        return None
    MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    date_string = date_string[:10]
    y, m, d = date_string.split('-')
    m = int(m)
    m = MONTHS[m-1]
    return str(d) + " " + m + " " + y


def process_text(body):
    soup = BeautifulSoup(body, features="html.parser")
    text = soup.text
    tags = ["<strong>", "</strong>", "<code>", "</code>", "<em>", "</em>", "\n", "<p>",
            "</p>", "'", '"', "</a>", "\n", "\\'", "\'", "<pre>", "</pre>", "\\\\", "\\", "\\n"]
    for tag in tags:
        text = text.replace(tag, "")
    return text.lower()


def get_question_by_id(id):
    url = "https://stackoverflow.com/questions/"+str(id)+"/"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    title = soup.find('a', class_="question-hyperlink").text
    body = process_text(soup.find('div', class_="post-text").text)

    vote_count = int(soup.find('div', class_='js-vote-count').text)

    is_answered = False
    for answered_icon in soup.find_all('div', class_='js-accepted-answer-indicator'):
        if 'd-none' not in answered_icon['class']:
            is_answered = True
            break

    owner = soup.find('div', class_='owner')
    creation_timestamp = owner.find('span', class_='relativetime')['title']

    question = {
        'id': id,
        'title': title,
        'body': body,
        'url': url,
        'is_answered': is_answered,
        'score': vote_count,
        'creation_timestamp': process_date(creation_timestamp),
        'owner': get_owner_details(owner)
    }
    return question


def get_owner_details(owner_obj):
    url = None
    if owner_obj.find('a') is not None:
        url = "https://stackoverflow.com" + owner_obj.find('a')['href']
    owner = {'url': url, 'name': None, 'score': 0,
             'gold': 0, 'silver': 0, 'bronze': 0, 'id': None}

    id = None
    if url is not None:
        temps = url.split('/')
        for item in temps:
            if re.match(r'[0-9]+', item):
                id = int(item)
                break

    user_details = owner_obj.find('div', class_='user-details')
    if user_details is not None:
        name = None
        if user_details.find('a') is not None:
            name = user_details.find('a').text
        owner['name'] = name

        reputation = 0
        if user_details.find('span', class_='reputation-score') is not None:
            reputation = int(re.sub(r'[^0-9]', '', user_details.find('span',
                                                                     class_='reputation-score').text))
        owner['score'] = reputation

        Flair = user_details.find('div', class_='-flair')
        gold = 0
        silver = 0
        bronze = 0
        if Flair is not None:
            for child in Flair.findChildren():
                if child.get('title') is not None:
                    if "gold" in child['title']:
                        gold = int(re.sub(r'[^0-9]', '', child['title']))
                    if "silver" in child['title']:
                        silver = int(re.sub(r'[^0-9]', '', child['title']))
                    if "bronze" in child["title"]:
                        bronze = int(re.sub(r'[^0-9]', '', child['title']))

        owner['gold'] = gold
        owner['silver'] = silver
        owner['bronze'] = bronze

    owner['id'] = id
    return owner


def get_answers_for_question(id):
    answers = []
    url = "https://stackoverflow.com/questions/"+str(id)+"/"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")

    for answer in soup.find_all('div', class_="answer"):
        ans_id = int(re.sub(r'[^0-9]', '', answer['id']))
        ans_url = "https://stackoverflow.com/a/"+str(ans_id)
        score = int(re.sub(r'[^0-9]', '', answer.find('div',
                                                      class_='js-vote-count')['data-value']))

        users = answer.find_all('div', class_='post-signature')
        owner_detail = None
        if len(users) != 0:
            owner_detail = users[len(users)-1]
        owner = {}

        timestamp = None
        if owner_detail is not None and owner_detail.find('a') is not None:
            owner = get_owner_details(owner_detail)
            timestamp = None
            if owner_detail.find('span', class_='relativetime') is not None:
                timestamp = owner_detail.find(
                    'span', class_='relativetime')['title']
        else:
            tempid = None
            owner = {
                'url': None,
                'name': 0,
                'gold': 0,
                'silver': 0,
                'bronze': 0,
                'score': 0,
                'id': tempid
            }
        answer_dict = {
            'id': ans_id,
            'score': score,
            'owner': owner,
            "url": ans_url,
            'creation_timestamp': process_date(timestamp)
        }

        if 'accepted-answer' in answer['class']:
            answer_dict['accepted'] = True
        else:
            answer_dict['accepted'] = False

        answers.append(answer_dict)

    return answers


def get_question_and_answers(id):
    question = get_question_by_id(id)
    answers = get_answers_for_question(id)
    return {
        'question': question,
        'answers': answers
    }


if __name__ == "__main__":
    id = 1522564  # 57082112
    pprint.pprint(get_question_and_answers(id))
