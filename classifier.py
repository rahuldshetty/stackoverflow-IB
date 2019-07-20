import math


def create_answers_vector(answers):
    vector = []
    for answer in answers:
        temp = [
            answer['url'], answer['owner']['name'], answer['score'], answer['owner']['score'], answer['owner']['gold'],
            answer['owner']['silver'], answer['owner']['bronze'], 1 if answer['accepted'] == True else 0
        ]
        vector.append(temp)
    return vector


def avg(data, col):
    s = 0
    for i in data:
        s += i[col]
    return s/len(data)


def avg_col(data, col_id):
    a = []
    s = 0
    for i in range(len(data)):
        col_ele = data[i][col_id]
        s += col_ele
    for i in range(len(data)):
        a.append(data[i][col_id]/s)
    return a


def equation_of_accept(row, avg_score, avg_rep, avg_gold, avg_silver, avg_bronze):
    if row[7] == 1:
        return 1.0
    score = row[2]
    rep = row[3]
    gold = row[4]
    silver = row[5]
    bronze = row[6]

    s = 0
    if score >= avg_score:
        s += 1

    if rep >= avg_rep:
        s += 1

    if gold >= avg_gold:
        s += 1
    elif silver >= avg_silver:
        s += 1
    elif bronze >= avg_bronze:
        s += 1

    val = s

    return 1/(1+math.exp(-val))


def set_col(matrix, col_id, new_col_data):
    for row in range(len(matrix)):
        matrix[row][col_id] = new_col_data[row]
    return matrix


def convert2String(vector):
    newVec = []
    for i in vector:
        newVec.append(str(i))
    return newVec


def process_predict(question_answer_obj, num_results):
    predicted_answers = []
    for item in question_answer_obj:
        temp_res = num_results
        answers = item['answers']
        vector = create_answers_vector(answers)

        avg_score = avg(vector, 2)
        avg_rep = avg(vector, 3)
        avg_gold = avg(vector, 4)
        avg_silver = avg(vector, 5)
        avg_bronze = avg(vector, 6)

        probabs = []
        for row in vector:
            probabs.append(equation_of_accept(
                row, avg_score, avg_rep, avg_gold, avg_silver, avg_bronze))

        for i in range(len(probabs)):
            if probabs[i] >= 0.5 and temp_res != 0:
                temp = convert2String(vector[i])
                predicted_answers.append(temp + [str(probabs[i])])
                temp_res -= 1
            if temp_res == 0:
                break
    predicted_answers = sorted(
        predicted_answers, key=lambda x: eval(x[8]), reverse=True)
    return predicted_answers
