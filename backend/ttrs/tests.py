import json

from django.contrib.auth.hashers import make_password
from django.test import TestCase, Client

from .models import College, Student, Department, Major, Course, Lecture, TimeSlot


class MyTestCase(TestCase):
    def setUp(self):
        # This comment is for crawling setUp.
        # I leave this implementation for the case that we must use crawled data
        #
        # admin = User(username='user', is_staff=True)
        # admin.set_password('password')
        # admin.save()
        # client = Client()
        # client.login(username='user', password='password')
        #
        # response = client.post('/manager/crawlers/', data={
        #     'year': 2018,
        #     'semester': '1학기',
        # })
        # crawler_id = response.json()['id']
        #
        # from time import sleep
        # for i in range(30):
        #     response = client.get('/manager/crawlers/{}/'.format(crawler_id))
        #     sleep(1)
        # assert 'running' in response.json()['status']
        #
        # client.put('/manager/crawlers/{}/'.format(crawler_id))
        # for i in range(30):
        #     response = client.get('/manager/crawlers/{}/'.format(crawler_id))
        #     if 'running' not in response.json()['status']:
        #         break
        #     sleep(1)
        # assert 'canceled' in response.json()['status']

        college1 = College.objects.create(name='college1')
        department1 = Department.objects.create(name='department1', college=college1)
        major1 = Major.objects.create(name='major1', department=department1)
        college2 = College.objects.create(name='college2')
        department2 = Department.objects.create(name='department2', college=college2)
        college3 = College.objects.create(name='college3')

        course1 = Course.objects.create(name='course1', code='code1', type='전필', grade=3, credit=4, college=college1, department=department1)
        course2 = Course.objects.create(name='course2', code='code2', type='전선', grade=2, credit=3, college=college1, department=department1, major=major1)
        course3 = Course.objects.create(name='course3', code='code3', type='교양', grade=1, credit=2, college=college2, department=department2)

        time_slot1 = TimeSlot.objects.create(day_of_week='월', start_time='12:00', end_time='13:15')
        time_slot2 = TimeSlot.objects.create(day_of_week='수', start_time='12:00', end_time='13:15')
        time_slot3 = TimeSlot.objects.create(day_of_week='금', start_time='16:00', end_time='18:00')
        lecture1 = Lecture.objects.create(course=course1, year=2018, semester='1학기', number='001', instructor='가나다', note='')
        lecture1.time_slots.add(time_slot1)
        lecture1.time_slots.add(time_slot2)
        lecture1.time_slots.add(time_slot3)

        time_slot1 = TimeSlot.objects.create(day_of_week='월', start_time='13:00', end_time='14:15')
        time_slot2 = TimeSlot.objects.create(day_of_week='수', start_time='13:00', end_time='14:15')
        time_slot3 = TimeSlot.objects.create(day_of_week='목', start_time='9:00', end_time='10:45')
        lecture1 = Lecture.objects.create(course=course1, year=2018, semester='1학기', number='002', instructor='ABC', note='RRR')
        lecture1.time_slots.add(time_slot1)
        lecture1.time_slots.add(time_slot2)
        lecture1.time_slots.add(time_slot3)

        time_slot1 = TimeSlot.objects.create(day_of_week='월', start_time='12:00', end_time='13:15')
        time_slot2 = TimeSlot.objects.create(day_of_week='수', start_time='12:00', end_time='13:15')
        time_slot3 = TimeSlot.objects.create(day_of_week='금', start_time='16:00', end_time='18:00')
        lecture1 = Lecture.objects.create(course=course2, year=2018, semester='1학기', number='001', instructor='가나다', note='')
        lecture1.time_slots.add(time_slot1)
        lecture1.time_slots.add(time_slot2)
        lecture1.time_slots.add(time_slot3)

        self.client = Client()
        self.sign_in()

    def sign_in(self):
        if not Student.objects.filter(username='stu1').exists():
            data = {
                'username': 'stu1',
                'password': make_password('password'),
                'email': 'stu1@snu.ac.kr',
                'grade': 3,
                'college_id': 1,
                'department_id': 1,
            }
            Student.objects.get_or_create(**data)
        self.assertTrue(self.client.login(username='stu1', password='password'))


class StudentViewTest(MyTestCase):
    url_my = '/ttrs/students/my/'

    def test_sign_up(self):
        response = self.client.post('/ttrs/students/signup/', data={
            'username': 'student',
            'password': 'paawsesfawword',
            'email': 'student@snu.ac.kr',
            'grade': 3,
            'college': 1,
            'department': 1,
        })
        print(response.json())
        self.assertEqual(response.status_code, 201)

    def test_my_retrieve(self):
        response = self.client.get(self.url_my)
        print(response.json())
        self.assertEqual(response.status_code, 200)

    def test_my_update_success(self):
        response = self.client.patch(self.url_my, data=json.dumps({'grade': 1}), content_type='application/json')
        print(response.json())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['grade'], 1)

    def test_my_update_fail(self):
        errors = [
            dict(password='password'),
            dict(email='email'),
            dict(email='stu1@gmail.com'),
            dict(college=-1),
            dict(college=1, department=2),
            dict(college=1, department=1, major=2),
        ]
        for error_input in errors:
            response = self.client.patch(self.url_my, data=json.dumps(error_input), content_type='application/json')
            print(response.json())
            self.assertEqual(response.status_code, 400)

    def test_my_delete(self):
        response = self.client.delete(self.url_my)
        print(response.status_code)
        self.assertEqual(response.status_code, 204)
