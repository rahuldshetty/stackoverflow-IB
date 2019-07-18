import urllib
import requests
import json
from bs4 import BeautifulSoup
import re
import pprint

'''
Custom Stackoverflow API for getting user,question and answer details
'''


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
    title = process_text(soup.find('a', class_="question-hyperlink").text)
    body = process_text(soup.find('div', class_="post-text").text)

    vote_count = int(soup.find('div', class_='js-vote-count').text)

    is_answered = False
    for answered_icon in soup.find_all('div', class_='js-accepted-answer-indicator'):
        if 'd-none' not in answered_icon['class']:
            is_answered = True
            break

    owner = soup.find('div', class_='owner')
    creation_timestamp = owner.find('span', class_='relativetime')['title']
    user_details = owner.find('div', class_='user-details')
    userlink = "https://stackoverflow.com" + \
        user_details.findChildren()[0]['href']

    question = {
        'id': id,
        'title': title,
        'body': body,
        'url': url,
        'is_answered': is_answered,
        'score': vote_count,
        'creation_timestamp': creation_timestamp,
        'owner': get_owner_details(userlink)
    }
    return question


def get_owner_details(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    owner = {'url': url}

    id = None
    temps = url.split('/')
    for item in temps:
        if re.match(r'[0-9]+', item):
            id = int(item)
            break

    name = soup.find(
        'h2', class_='profile-user--name').find('div', class_='grid--cell').text
    owner['name'] = name

    reputation = int(re.sub(r'[^0-9]', '', soup.find('div',
                                                     class_='my12').find('div', class_='fs-title').text))
    owner['score'] = reputation

    gold = int(re.sub(r'[^0-9]', '', soup.find('div',
                                               class_='badge1-alternate')['title']) if soup.find('div',
                                                                                                 class_='badge1-alternate') is not None else '0')
    silver = int(re.sub(r'[^0-9]', '', soup.find('div',
                                                 class_='badge2-alternate')['title'] if soup.find('div',
                                                                                                  class_='badge2-alternate') is not None else '0'))
    bronze = int(re.sub(r'[^0-9]', '', soup.find('div',
                                                 class_='badge3-alternate')['title'] if soup.find('div',
                                                                                                  class_='badge3-alternate') is not None else '0'))

    owner['gold'] = gold
    owner['silver'] = silver
    owner['bronze'] = bronze
    owner['id'] = id

    count_ele = soup.find('div', class_='fc-medium mb16')
    items = count_ele.find_all('div', class_='fc-dark')
    answer_count = int(re.sub('[^0-9]', '', items[0].text))
    question_count = int(re.sub('[^0-9]', '', items[1].text))

    owner['answer_count'] = answer_count
    owner['question_count'] = question_count

    return owner


def get_answers_for_question(id):
    answers = []
    url = "https://stackoverflow.com/questions/"+str(id)+"/"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")

    for answer in soup.find_all('div', class_="answer"):
        ans_id = int(re.sub(r'[^0-9]', '', answer['id']))

        score = int(re.sub(r'[^0-9]', '', answer.find('div',
                                                      class_='js-vote-count')['data-value']))

        users = answer.find_all('div', class_='post-signature')
        owner_detail = users[len(users)-1]
        owner_url = "https://stackoverflow.com" + \
            owner_detail.find('a')['href']

        answer_dict = {
            'id': ans_id,
            'score': score,
            'owner': get_owner_details(owner_url)
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
