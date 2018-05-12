print('Cleaning models...')

def clean_crawlers():
    from manager.models import Crawler

    crawlers = Crawler.objects.all()
    print('Crawler:', crawlers)

    for crawler in crawlers:
        try:
            print('Deleting crawler {}...'.format(crawler.id))
            crawler.delete()

        except Exception as e:
            print(e)


def clean_students():
    from ttrs.models import Student
    
    students = Student.objects.all()
    print('Student:', students)

    for student in students:
        try:
            print('Deleting student {}...'.format(student.username))
            student.delete()

        except Exception as e:
            print(e)


def clean_colleges():
    from ttrs.models import College

    colleges = College.objects.all()
    print('College:', colleges)

    for college in colleges:
        try:
            print('Deleting college {}...'.format(college.id))
            college.delete()

        except Exception as e:
            print(e)


def clean_classrooms():
    from ttrs.models import Classroom

    classrooms = Classroom.objects.all()
    print('Classroom:', classrooms)

    for classroom in classrooms:
        try:
            print('Deleting classroom {}...'.format(classroom.id))
            classroom.delete()

        except Exception as e:
            print(e)


clean_crawlers()
clean_students()
clean_colleges()
clean_classrooms()
