import random

from django.db.models import Max, Min

from ttrs.models import Lecture, TimeTable

# Option fields and their default values
option_field = {
    'year': 2018,
    'semester': '1학기',
    'expected_credit': 15,
    'credit_weight': 0,
    'distance_weight': 0,
    'evaluation_weight': 0,
    'first_period_weight': 0,
    'serial_lectures_weight': 0,
}


def recommend(options, student):
    info = {}
    for option in option_field.keys():
        info[option] = options[option] if options.get(option) else option_field[option]

    # Convert values to int
    for key in info.keys():
        if key == 'semester':
            continue
        info[key] = int(info[key])

    lectures = Lecture.objects.filter(year=info['year'], semester=info['semester'])
    info['min_id'] = lectures.aggregate(min_id=Min('id'))['min_id']
    info['max_id'] = lectures.aggregate(max_id=Max('id'))['max_id']

    print(info)
    recommends = []
    num_candidates = 50
    num_recommends = 3
    for i in range(num_candidates):
        print('table', i)
        time_table = build_timetable(info)
        recommends.append(time_table)

    recommends.sort(key=lambda x: get_score(x, info, student), reverse=True)
    print([get_score(x, info, student) for x in recommends])
    for time_table in recommends:
        time_table.delete()
    return recommends[:num_recommends]


def build_timetable(info):
    lectures = get_lectures(info['expected_credit'], Lecture.objects.filter(year=info['year'], semester=info['semester']), [], info)
    time_table = TimeTable(title='table', year=info['year'], semester=info['semester'])
    time_table.save()
    for lecture in lectures:
        time_table.lectures.add(lecture)
    return time_table


def get_lectures(remain_credit, remain_lectures, lectures, info):
    if -3 < remain_credit < 3:
        return lectures
    while True:
        if random.randint(1, 20)==1:
            return lectures
        lecture = get_random_object(remain_lectures, info['min_id'], info['max_id'])
        lectures.append(lecture)
        if not Lecture.have_same_course(lectures) and not Lecture.do_overlap(lectures):
            break
        lectures = lectures[:-1]
    remain_lectures.exclude(id=lecture.id)
    remain_credit -= lecture.course.credit
    return get_lectures(remain_credit, remain_lectures, lectures, info)


def get_random_object(objects, min_id, max_id):
    while True:
        pk = random.randint(min_id, max_id)
        instance = objects.filter(pk=pk).first()
        if instance:
            return instance


def get_score(time_table, info, student):
    total_score = 0
    total_credit = 0
    for lecture in time_table.lectures.all():
        lecture_score = 0
        course = lecture.course
        total_credit += course.credit

        if course.type == '교양':
            lecture_score += 1
        if course.department and student.department and course.department == student.department:
            print(course.department, student.department)
            lecture_score += 2
        if course.major and student.major and course.major == student.major:
            print(course.major, student.major)
            lecture_score += 3
            if course.type == '전선':
                lecture_score += 3
            if course.type == '전필':
                lecture_score += 6

        # Reduce lecture score if it has first period.
        for time_slot in lecture.time_slots.all():
            if time_slot.start_time < '10:00':
                total_score -= info['first_period_weight']

        # Reduce lecture score if it has bad evaluations.
        evaluations = lecture.evaluations.all()
        if len(evaluations) != 0:
            rate = 0
            for evaluation in evaluations:
                rate += evaluation.rate
            rate /= len(lecture.evaluations.all())
            lecture_score -= (5-rate)*info['evaluation_weight']

        # Add lecture score to total score.
        total_score += lecture_score*course.credit

    # Reduce total score if there are serial lectures.
    serial_lectures = get_serial_lectures(time_table)
    for pair in serial_lectures:
        total_score -= info['serial_lectures_weight']

    # TODO: Reduce total score if classrooms are far away

    # Reduce total score if total credit is different from expected credit.
    total_score -= abs(total_credit-info['expected_credit'])*info['credit_weight']
    return total_score


def get_serial_lectures(time_table):
    """
    Given time_table, returns a set of pairs of temporally adjacent lectures.
    :param time_table:
    :return serial_lectures:
    """
    serial_lectures = set()

    lectures = time_table.lectures.all()
    for lec1 in lectures:
        for lec2 in lectures:
            if lec1 == lec2:
                continue

            for time_slot1 in lec1.time_slots.all():
                start_time1 = list(map(int, time_slot1.start_time.split(':')))
                start_time1 = 60*start_time1[0] + start_time1[1]
                end_time1 = list(map(int, time_slot1.end_time.split(':')))
                end_time1 = 60*end_time1[0] + end_time1[1]

                for time_slot2 in lec2.time_slots.all():
                    start_time2 = list(map(int, time_slot2.start_time.split(':')))
                    start_time2 = 60*start_time2[0] + start_time2[1]
                    end_time2 = list(map(int, time_slot2.end_time.split(':')))
                    end_time2 = 60*end_time2[0] + end_time2[1]

                    if end_time1 < start_time2 < end_time1 + 30:
                        serial_lectures.add((lec1.id, lec2.id))

                    if end_time2 < start_time1 < end_time2 + 30:
                        serial_lectures.add((lec2.id, lec1.id))

    print(serial_lectures)
    return serial_lectures
