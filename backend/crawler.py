from selenium import webdriver

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

import django
django.setup()

from ttrs.models import *

sid = {'1학기': 1,
       '2학기': 2,
       '여름학기': 3,
       '겨울학기': 4
}

day = {'월': '2018-05-07T',
       '화': '2018-05-08T',
       '수': '2018-05-08T',
       '목': '2018-05-08T',
       '금': '2018-05-08T',
       '토': '2018-05-08T',
       '일': '2018-05-08T',
}

def crawl(semester):
    driver = webdriver.Chrome('/home/newlame/PycharmProjects/untitled/chromedriver')
    driver.implicitly_wait(3)

    driver.get('https://sugang.snu.ac.kr/sugang/cc/cc100.action')
    driver.find_element_by_id('detail_button').click()
    driver.find_element_by_xpath('//*[@id="srchOpenShtm"]/option[{}]'.format(sid[semester])).click()
    driver.find_element_by_xpath('//*[@id="srchOpenSubmattCorsFg"]/option[2]').click()
    #driver.find_element_by_id('srchSbjtCd').send_keys('')
    #driver.find_element_by_id('srchSbjtNm').send_keys('')
    driver.find_element_by_class_name('btn_search_ok').click()

    page_end = int(driver.find_element_by_xpath('//*[@id="content"]/div/div[3]/div[1]/div[1]/h3/span').text)//10 + 1

    lectures = []
    errors = []

    for i in range(1, 2):
        print('crawling page {}'.format(i))
        driver.execute_script('fnGotoPage({})'.format(i))
        elts = driver.find_element_by_xpath('//*[@id="content"]/div/div[3]/div[1]/div[2]/table/tbody')
        lecture = None
        for row in elts.find_elements_by_tag_name('tr'):
            try:
                columns = row.find_elements_by_tag_name('td')
                if not columns[0].text:
                    if lecture is not None:
                        lectures.append(lecture)
                        #print(i, lecture)
                    lecture = {
                        'semester': semester,
                        'type': columns[1].text,
                        'name': columns[8].text,
                        'department': columns[3].text,
                        'college': columns[2].text,
                        'grade': columns[5].text,
                        'instructor': columns[13].text,
                        'code': columns[6].text,
                        'number': columns[7].text,
                        'credit': columns[9].text,
                    }

                    if not columns[12].text:
                        raise Exception('No time slot')
                    time_slot = {
                        'time': columns[10].text,
                        'classroom': {
                            'building': columns[12].text.split('-')[0],
                            'room_no': columns[12].text.split('-')[1],
                        }
                    }

                    lecture['time_slots'] = [time_slot]

                else:
                    if not columns[2].text:
                        raise Exception('No time slot')

                    time_slot = {
                        'time': columns[0].text,
                        'classroom': {
                            'building': columns[2].text.split('-')[0],
                            'room_no': columns[2].text.split('-')[1],
                        }
                    }

                    lecture['time_slots'].append(time_slot)
            except Exception as e:
                errors.append(str(e))

    #print(errors)
    driver.close()
    return lectures


if __name__ == '__main__':
    lectures = crawl('여름학기')
    for lecture in lectures:
        college = College.objects.create(name=lecture['college'])
        college.save()

        department = Department.objects.create(college=college,
                                               name=lecture['department'])
        department.save()

        c = Course.objects.create(code=lecture['code'],
                                  name=lecture['name'],
                                  type=lecture['type'],
                                  #field=,
                                  grade=int(lecture['grade'][0]),
                                  credit=int(lecture['credit'].split('-')[0]),
                                  college=college,
                                  department=department,
                                  #major=
                                  )
        c.save()

        l = Lecture.objects.create(course=c,
                                   year=2018,
                                   semester=lecture['semester'],
                                   number=lecture['number'],
                                   instructor=lecture['instructor'],
                                   note='')

        for time_slot in lecture['time_slots']:
            cr = Classroom.objects.create(building=time_slot['classroom']['building'],
                                          room_no=time_slot['classroom']['room_no'])
            cr.save()

            print(day[time_slot['time'][0]], time_slot['time'][2:7], time_slot['time'][8:13])

            ts = TimeSlot.objects.create(start=day[time_slot['time'][0]] + time_slot['time'][2:7] + 'Z',
                                         end=day[time_slot['time'][0]] + time_slot['time'][8:13] + 'Z',
                                         classroom=cr)
            ts.save()
            l.time_slots.add(ts)





