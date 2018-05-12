
def student_test(uid, upwd):
    auth = (uid, upwd)
    link = 'http://localhost:8000/ttrs/students/signup/'

    import requests
    for i in range(1,6):
        data = {}
        data['username'] = 'stu{}'.format(i)
        data['password'] = 'qwertyasdf'
        data['email'] = 'stu{}@snu.ac.kr'.format(i)
        data['grade'] = 1

        from ttrs.models import College
        data['college'] = College.objects.all()[0].id

        print('Creating student {}...'.format(i))
        res = requests.post(link, auth=auth, data=data)

        if res.status_code == 201:
                print('Successfully created Student instance.')
        else:
                print('Error creating Student instance.')
                print(res.text)
