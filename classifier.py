
def create_answers_vector(answers):
    vector = []
    for answer in answers:
        temp = [
            answer['url'], answer['owner']['name'], answer['score'], answer['owner']['score'], answer['owner']['gold'],
            answer['owner']['silver'], answer['owner']['bronze'], 1 if answer['accepted'] == True else 0
        ]
        vector.append(temp)
    return vector


def avg_col(data, col_id):
    a = []
    s = 0
    for i in range(len(data)):
        col_ele = data[i][col_id]
        s += col_ele
    for i in range(len(data)):
        a.append(data[i][col_id]/s)
    return a


def set_col(matrix, col_id, new_col_data):
    for row in range(len(matrix)):
        matrix[row][col_id] = new_col_data[row]
    return matrix


def process_predict(question_answer_obj):
    predicted_answers = []
    for item in question_answer_obj:
        answers = item['answers']
        vector = create_answers_vector(answers)
        avg_score = avg_col(vector, 2)
        avg_rep = avg_col(vector, 3)

        vector = set_col(vector, 2, avg_score)
        vector = set_col(vector, 3, avg_rep)
        print(vector)

    return predicted_answers
