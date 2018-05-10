import json
import random


def recommend(_options):
    try:
        options = json.loads(_options)

        print(options)

        recommends = {}
        num_recommends = 3
        for i in range(num_recommends):
            lectures = build_timetable(options)
            score = get_score(lectures, options)

            recommends['tt {}'.format(i)] = {"lectures": lectures, "score": score}

        return recommends

    except Exception as e:
        print(e)


def build_timetable(options):
    if 'student_id' in options:
        student_id = int(options.get('student_id'))
        # grab some info about student from db

    expected_credit = int(options.get('expected_credit')) if 'expected_credit' in options else 18
        
    # some recursive method to construct tt?
    lectures = []
    for j in range(expected_credit):
        lecture_id = random.randrange(1,100)
        lectures.append(lecture_id)

    return lectures


def get_score(lectures, options):
    return random.randrange(1,100)
