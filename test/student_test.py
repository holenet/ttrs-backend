
def student_test(uid, upwd):
    auth = (uid, upwd)
    base = 'http://localhost:8000/ttrs/students/'
    signup = base+'signup/'
    my = base+'my/'

    import requests
    print()
    print('testing '+'\033[1m'+signup+'\033[0m'+'...')
    for i in range(1,6):
        data = {}
        data['username'] = 'stu{}'.format(i)
        data['password'] = 'qwertyasdf'
        data['email'] = 'stu{}@snu.ac.kr'.format(i)
        data['grade'] = 1

        from ttrs.models import College
        data['college'] = College.objects.all()[0].id

        print('Creating student {}...'.format(i))
        res = requests.post(signup, data=data)

        if res.status_code == 201:
            print('Successfully created Student instance.')
        else:
            print('Error creating Student instance.')
            print(res.text)

    print()
    print('testing '+'\033[1m'+base+'\033[0m'+'...')
    res = requests.get(base, auth=auth)
    if res.status_code == 200:
        print('Successfully accessed Student list.')
    else:
        print('Error accessing Student list.')
