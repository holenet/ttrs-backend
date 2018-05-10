import json
import random


def recommend(_options):
    try:
        options = json.loads(_options)

        recommends = {}
        num_recommends = 3
        for i in range(num_recommends):
            lectures = build_timetable(options)
            score = get_score(lectures)

            recommends['tt {}'.format(i)] = (lectures, score)

        return json.dumps(recommends)

    except Exception as e:
        print(e)


def build_timetable(options):
    lectures = []

    if 'student_id' in options:
        student_id = int(options.get('student_id'))
        # grab some info about student from db

    expected_credit = int(options.get('expected_credit')) if 'expected_credit' in options else 18
        
    # some recursive method to construct tt?
    for j in range(expected_credit):
        lecture_id = random.randrange(1,100)
        lectures.append(lecture_id)

    return lectures


def get_score(lectures):
    return random.randrange(1,100)
