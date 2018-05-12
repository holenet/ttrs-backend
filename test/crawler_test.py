import requests
import time

def crawler_test(uid, upwd):
    auth = (uid, upwd)
    link = 'http://localhost:8000/manager/crawlers/'
    data = {'year':'2018', 'semester':'1학기'}

    # I don't know the reason, but it works only if requests is imported here.
    # Do you know why?
    import requests
    print('Creating crawler', data, '...')
    res = requests.post(link, auth=auth, data=data)
    if res.status_code == 201:
        print('Successfully created Crawler instance.')

        # Here too.
        import json
        cid = json.loads(res.text)['id']
        print('Running Crawler {}...'.format(cid))

        # Here too... :(
        import time
        time.sleep(30)

        print('Stopping Crawler instance...')
        if requests.put(link+str(cid)+'/', auth=auth).status_code == 200:
            print('Successfully stopped Crawler instance.')
        else:
            print('Error stopping Crawler instance.')
    else:
        print('Error creating Crawler instance.')

