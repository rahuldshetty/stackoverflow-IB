from flask import *
from classifier import *
from os import environ
from indexer import *

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


if __name__ == "__main__":
    app.run(debug=True,  # host='0.0.0.0',
            port=environ.get("PORT", 5000), threaded=False)
