import random

from django.core.exceptions import ObjectDoesNotExist

from .models import Student


def recommend(options):
    print(options)

    recommends = []
    num_recommends = 3
    for i in range(num_recommends):
        lectures = build_timetable(options)
        score = get_score(lectures, options)

        recommends.append({"lectures": lectures, "score": score})

    return recommends


def build_timetable(options):
    if 'student_id' in options:
        try:
            student_id = int(options.get('student_id'))
            student = Student.objects.get(id=student_id)

            # grab some info..
            college = student.college
            department = student.department
            major = student.major
            not_recommends = [lec.id for lec in student.not_recommends.all()]

            print(college, department, major, not_recommends)

        except ObjectDoesNotExist as e:
            print(e)
            return


    expected_credit = int(options.get('expected_credit')) if 'expected_credit' in options else 15
        
    # some recursive method to construct tt?
    lectures = []
    for j in range(expected_credit):
        lecture_id = random.randrange(1,100)
        lectures.append(lecture_id)

    return lectures


def get_score(lectures, options):
    return random.randrange(1,100)
