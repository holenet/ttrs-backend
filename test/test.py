import os, sys
from django.conf import settings

test_path = os.path.join(settings.BASE_DIR, '../test/')
sys.path.append(test_path)

from crawler_test import crawler_test
from student_test import student_test

uid = 'lame'
upwd = 'qwertyasdf'

print()
print('\033[1m'+'='*15, 'Crawler Test', '='*15+'\033[0m')
crawler_test(uid, upwd)

print()
print('\033[1m'+'='*15, 'Student Test', '='*15+'\033[0m')
student_test(uid, upwd)
