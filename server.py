from flask import *
from google_search import *
from classifier import *

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search', methods=['POST'])
def search():
    text = request.form['query']
    number = int(request.form['numberresults'])
    quest_answers = get_all_question_and_answers(text=text, num_results=number)

    answers = process_predict(quest_answers)

    settings = {
        "num_results": number
    }

    return render_template('search.html', text=text, data=quest_answers, settings=settings, answers=answers)


if __name__ == "__main__":
    app.run(debug=True)
