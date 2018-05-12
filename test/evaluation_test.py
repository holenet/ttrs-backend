
def evaluation_test(uid, upwd):
    auth = (uid, upwd)
    base = 'http://localhost:8000/ttrs/evaluations/'

    import json, requests
    from ttrs.models import Lecture

    print('\ntesting'+'\033[1m'+base+'\033[0m'+'...')
    for i in range(1,4):
        data = {}
        data['rate'] = 5
        data['comment'] = 'Wonderful lecture!'
        data['lecture'] = Lecture.objects.all()[i].id

        print('\nCreating Evaluation {}...'.format(i))
        res = requests.post(base, auth=('stu1', 'qwertyasdf'), data=data)

        if res.status_code == 201:
            print('Successfully created Evaluation instance.')
            print(res.text)
        else:
            print('Error creating Evaluation instance.')
            print(res.text)

