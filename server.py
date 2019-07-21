from flask import *
from classifier import *
from os import environ
from indexer import *
import requests

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.errorhandler(404)
def not_found(e):
    return render_template('error.html')


@app.route('/search', methods=['POST'])
def search():
    text = request.form['query']
    number = int(request.form['numberresults'])
    result_count = int(request.form['num_search_results'])

    quest_answers = get_all_question_and_answers(text, number)

    answers = process_predict(quest_answers, result_count)

    settings = {
        "num_results": number
    }

    return render_template('search.html', text=text, data=quest_answers, settings=settings, answers=answers)


def download():
    link = 'https://raw.githubusercontent.com/rahuldshetty/stackoverflow-IBM/master/indexdir/MAIN_sru8vf8i6mlyp5l3.seg'
    path = 'indexdir/MAIN_sru8vf8i6mlyp5l3.seg'
    r = requests.get(link)
    with open(path, 'wb') as f:
        f.write(r.content)


if __name__ == "__main__":
    if os.path.exists('indexdir/MAIN_sru8vf8i6mlyp5l3.seg') == False:
        download()
    app.run(debug=True,  host='0.0.0.0',
            port=environ.get("PORT", 5000), threaded=False)
