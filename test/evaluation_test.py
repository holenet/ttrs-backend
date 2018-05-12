
def evaluation_test(uid, upwd):
    auth = (uid, upwd)
    base = 'http://localhost:8000/ttrs/evaluations/'

    import json, requests
    from ttrs.models import Lecture

    print('\ntesting '+'\033[1m'+base+'\033[0m'+'...')
    for i in range(1,4):
        data = {}
        data['rate'] = 5
        data['comment'] = 'Wonderful lecture!'
        data['lecture'] = Lecture.objects.all()[i].id

        print('\nCreating Evaluation {}...'.format(i))
        res = requests.post(base, auth=auth, data=data)

        if res.status_code == 201:
            print('Successfully created Evaluation instance.')
            print(res.text)
        else:
            print('Error creating Evaluation instance.')
            print(res.text)

    print('\n'+'\033[1m'+'testing invalid data...'+'\033[0m')
    data = {}
    data['rate'] = 99
    data['comment'] = ''
    data['lecture'] = 0

    res = requests.post(base, auth=auth, data=data)
    print(res)
    errors = json.loads(res.text)
    for error in errors:
        print(error, errors.get(error))
