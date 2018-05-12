import os, sys
from django.conf import settings

test_path = os.path.join(settings.BASE_DIR, '../test/')
sys.path.append(test_path)

from crawler_test import crawler_test
from student_test import student_test
from lecture_test import lecture_test
from evaluation_test import evaluation_test

uid = 'lame'
upwd = 'qwertyasdf'

print()
print('\033[1m'+'='*15, 'Crawler Test', '='*15+'\033[0m')
crawler_test(uid, upwd)

print()
print('\033[1m'+'='*15, 'Student Test', '='*15+'\033[0m')
student_test(uid, upwd)

print()
print('\033[1m'+'='*15, 'Lecture Test', '='*15+'\033[0m')
lecture_test(uid, upwd)

print('\n'+'\033[1m'+'='*15, 'Evaluation Test', '='*15+'\033[0m')
evaluation_test(uid, upwd)
