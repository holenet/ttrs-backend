import random

from django.db.models import Max, Min

from ttrs.models import Lecture, TimeTable


def recommend(options, student):
    info = {}
    info['year'] = int(options.get('year', None))
    info['semester'] = options.get('semester', None)
    if not info['year'] or not info['semester']:
        return []
    info['expected_credit'] = int(options.get('expected_credit', 15))

    print(info)
    recommends = []
    num_candidates = 100
    num_recommends = 3
    for i in range(num_candidates):
        print('table', i)
        time_table = build_timetable(info)
        recommends.append(time_table)
    recommends.sort(key=lambda x: get_score(x, info, student), reverse=True)
    print([get_score(x, info, student) for x in recommends])
    return recommends[:num_recommends]


def build_timetable(info):
    lectures = get_lectures(info['expected_credit'], Lecture.objects.filter(year=info['year'], semester=info['semester']), [])
    time_table = TimeTable(title='table', year=info['year'], semester=info['semester'])
    time_table.save()
    for lecture in lectures:
        time_table.lectures.add(lecture)
    return time_table


def get_lectures(remain_credit, remain_lectures, lectures):
    if -3 < remain_credit < 3:
        return lectures
    while True:
        if random.randint(1, 20)==1:
            return lectures
        lecture = get_random_object(remain_lectures)
        lectures.append(lecture)
        if not Lecture.have_same_course(lectures) and not Lecture.does_overlap(lectures):
            break
        lectures = lectures[:-1]
    remain_lectures.exclude(id=lecture.id)
    remain_credit -= lecture.course.credit
    return get_lectures(remain_credit, remain_lectures, lectures)


def get_random_object(objects):
    min_id = objects.aggregate(min_id=Min('id'))['min_id']
    max_id = objects.aggregate(max_id=Max('id'))['max_id']
    while True:
        pk = random.randint(min_id, max_id)
        instance = objects.filter(pk=pk).first()
        if instance:
            return instance


def get_score(time_table, info, student):
    score = 0
    total_credit = 0
    for lecture in time_table.lectures.all():
        course = lecture.course
        total_credit += course.credit
        if course.college == student.college:
            score += 1
        if course.department and course.department == student.department:
            score += 2
        if course.major and course.major == student.major:
            score += 3
            if course.type == '전선':
                score += 3
            if course.type == '전필':
                score += 3
    score += info['expected_credit']**2
    return score
