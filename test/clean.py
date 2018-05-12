
def clean_crawlers():
    from manager.models import Crawler

    crawlers = Crawler.objects.all()
    print('Deleting Crawler instances:', crawlers)
    crawlers.delete()


def clean_students():
    from ttrs.models import Student
    
    students = Student.objects.all()
    print('Deleting Student instances:', students)
    students.delete()


def clean_colleges():
    from ttrs.models import College

    colleges = College.objects.all()
    print('Deleting College instances:', colleges)
    colleges.delete()


def clean_classrooms():
    from ttrs.models import Classroom

    classrooms = Classroom.objects.all()
    print('Deleting Classroom instances:', classrooms)
    classrooms.delete()


print('\033[1m'+'='*15+' Initialize '+'='*15+'\033[0m')
clean_crawlers()
clean_students()
clean_colleges()
clean_classrooms()
print()
print('Successfully cleaned model instances.')
