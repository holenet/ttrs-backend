
def lecture_test(uid, upwd):
    auth = (uid, upwd)
    base = 'http://localhost:8000/ttrs/lectures/'

    import requests
    print()
    print('testing '+'\033[1m'+base+'\033[0m'+'...')
    
    res = requests.get(base, auth=auth)
    if res.status_code == 200:
        print('Successfully accessed Lecture list.')
    else:
        print('Error accessing Lecture list.')


    from ttrs.models import Lecture
    lecture = Lecture.objects.all()[0]

    filter = base+'?id='+str(lecture.id)
    print()
    print('testing '+'\033[1m'+filter+'\033[0m'+'...')
    res = requests.get(filter, auth=auth)
    if res.status_code == 200:
        print('Successfully accessed Lecture list with payload.')
    else:
        print('Error accessing Lecture list with keyword.')

    detail = base+str(lecture.id)+'/'
    print()
    print('testing '+'\033[1m'+detail+'\033[0m'+'...')
    res = requests.get(detail, auth=auth)
    if res.status_code == 200:
        print('Successfully accessed Lecture detail.')
    else:
        print('Error accessing Lecture detail.')
