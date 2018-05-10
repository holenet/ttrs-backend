import json
import random

def recommend(_options):
    try:
        options = json.loads(_options)
        print(options)

        student_id = int(options.get('student_id'))
        expected_credit = int(options.get('expected_credit'))

        recommends = {}
        num_recommends = 3
        for i in range(num_recommends):
            lectures = build_timetable(student_id, expected_credit)
            score = get_score(lectures)

            print('tt {}:'.format(i), lectures, score)

            recommends['tt {}'.format(i)] = (lectures, score)

        print(json.dumps(recommends))
        return json.dumps(recommends)

    except Exception as e:
        print(e)


def build_timetable(student_id, expected_credit):
    lectures = []
    for j in range(expected_credit):
        lecture_id = random.randrange(1,100)
        lectures.append(lecture_id)

    return lectures

def get_score(lectures):
    return random.randrange(1,100)
