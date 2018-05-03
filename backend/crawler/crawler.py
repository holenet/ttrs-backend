"""
function run is called by view with argument crawler.
while crawling the site, it updates status of the crawler and
checks cancel_flag of it.
If cancel_flag is True, it stops current job and set status to 'canceled'.
"""

import os
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from selenium import webdriver

from ttrs.models import *

driver_path = os.path.join(settings.BASE_DIR, '../chromedriver')

sid = {'1학기': 1,
       '2학기': 2,
       '여름학기': 3,
       '겨울학기': 4
       }


def run(crawler):
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1920x1080')
        options.add_argument('disable-gpu')
        options.add_argument('User-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KTHML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')

        driver = webdriver.Chrome(driver_path, chrome_options=options)
        driver.implicitly_wait(3)

        driver.get('https://sugang.snu.ac.kr/sugang/cc/cc100.action')
        driver.implicitly_wait(1)
        driver.find_element_by_id('detail_button').click()
        driver.implicitly_wait(1)
        driver.find_element_by_xpath('//*[@id="srchOpenSchyy"]').clear()
        driver.implicitly_wait(1)
        driver.find_element_by_xpath('//*[@id="srchOpenSchyy"]').send_keys(crawler.year)
        driver.implicitly_wait(1)
        driver.find_element_by_xpath('//*[@id="srchOpenShtm"]/option[{}]'.format(sid[crawler.semester])).click()
        driver.implicitly_wait(1)
        driver.find_element_by_xpath('//*[@id="srchOpenSubmattCorsFg"]/option[2]').click()
        driver.implicitly_wait(1)
        driver.find_element_by_class_name('btn_search_ok').click()
        driver.implicitly_wait(1)

        total_cnt = int(driver.find_element_by_xpath('//*[@id="content"]/div/div[3]/div[1]/div[1]/h3/span').text)
        total_page = ((total_cnt-1)//10)+1

        for i in range(1, total_page+1):
            # refresh crawler dynamically
            crawler.refresh_from_db()
            if crawler.cancel_flag:
                # administrator canceled this crawler
                crawler.status = 'canceled {}/{}'.format(i, total_page)
                crawler.save()
                return

            # goes to page i
            driver.execute_script('fnGotoPage({})'.format(i))
            # crawls a table of lectures in current page
            lectures = crawl(driver)
            # parses given data and saves it in DB
            parse(crawler.year, crawler.semester, lectures)

            # change status of crawler and save
            crawler.refresh_from_db()
            crawler.status = 'running {}/{}'.format(i, total_page)
            crawler.save()

        # finish crawling
        crawler.status = 'finished {}'.format(total_page)
        crawler.save()

        driver.close()

    except ObjectDoesNotExist as e:
        print(e)

    except Exception as e:
        crawler.status = str(e)
        crawler.save()


def crawl(driver):
    lectures = []
    errors = []

    # 'elts' is a table of lectures displayed in current page
    elts = driver.find_element_by_xpath('//*[@id="content"]/div/div[3]/div[1]/div[2]/table/tbody')
    lecture = None
    for row in elts.find_elements_by_tag_name('tr'):
        try:
            columns = row.find_elements_by_tag_name('td')

            if not columns[0].text:
                if lecture is not None:
                    lectures.append(lecture)

                if columns[3].text.split('(')[0] != columns[3].text:
                    department = columns[3].text.split('(')[0]
                    major = columns[3].text.split('(')[1].split(')')[0]
                else:
                    department = columns[3].text
                    major = ''

                lecture = {
                    'type': columns[1].text,
                    'name': columns[8].text,
                    'college': columns[2].text,
                    'department': department,
                    'major': major,
                    'grade': columns[5].text,
                    'instructor': columns[13].text,
                    'code': columns[6].text,
                    'number': columns[7].text,
                    'credit': columns[9].text,
                }

                if not columns[12].text:
                    raise Exception('No time slot')

                classroom = columns[12].text.split('-')
                if len(classroom) == 3:
                    #print(classroom)

                    if len(classroom[1]) == 1:
                        building = classroom[0] + '-' + classroom[1]
                        room_no = classroom[2]

                    else:
                        building = classroom[0]
                        room_no = classroom[1] + '-' + classroom[2]

                else:
                    building = classroom[0]
                    room_no = classroom[1]

                time_slot = {
                    'time': columns[10].text,
                    'classroom': {
                        'building': building,
                        'room_no': room_no,
                    }
                }

                lecture['time_slots'] = [time_slot]

            else:
                if not columns[2].text:
                    raise Exception('No time slot')

                classroom = columns[2].text.split('-')
                if len(classroom) == 3:
                    #print(classroom)

                    if len(classroom[1]) == 1:
                        building = classroom[0] + '-' + classroom[1]
                        room_no = classroom[2]

                    else:
                        building = classroom[0]
                        room_no = classroom[1] + '-' + classroom[2]

                else:
                    building = classroom[0]
                    room_no = classroom[1]

                time_slot = {
                    'time': columns[0].text,
                    'classroom': {
                        'building': building,
                        'room_no': room_no,
                    }
                }

                lecture['time_slots'].append(time_slot)
        except Exception as e:
            errors.append(str(e))

    return lectures


def parse(year, semester, lectures):
    for lecture in lectures:
        try:
            college_instance = College.objects.get(name=lecture['college'])
        except Exception as e:
            college_instance = College.objects.create(name=lecture['college'])
            college_instance.save()

        try:
            department_instance = Department.objects.get(name=lecture['department'])
        except Exception as e:
            if lecture['department'] != '':
                department_instance = Department.objects.create(college=college_instance,
                                                            name=lecture['department'])
                department_instance.save()

            else:
                department_instance = None

        try:
            major_instance = Major.objects.get(name=lecture['major'])
        except Exception as e:
            if lecture['major'] != '':
                major_instance = Major.objects.create(department=department_instance,
                                                  name=lecture['major'])
                major_instance.save()

            else:
                major_instance = None

        try:
            course_instance = Course.objects.get(name=lecture['name'])

        except Exception as e:
            course_instance = Course.objects.create(code=lecture['code'],
                                                    name=lecture['name'],
                                                    type=lecture['type'],
                                                    # field=,
                                                    grade=int(lecture['grade'][0]),
                                                    credit=int(lecture['credit'].split('-')[0]),
                                                    college=college_instance,
                                                    department=department_instance,
                                                    major=major_instance,
                                                    )
            course_instance.save()

        lecture_instance = Lecture.objects.create(course=course_instance,
                                                  year=year,
                                                  semester=semester,
                                                  number=lecture['number'],
                                                  instructor=lecture['instructor'],
                                                  note='')

        # It really is absurd, but there exists lectures without any time slot.
        try:
            for time_slot in lecture['time_slots']:
                try:
                    classroom_instance = Classroom.objects.get(whole=time_slot['classroom']['building'] + '-'
                                                                     + time_slot['classroom']['room_no'])
                except Exception as e:
                    classroom_instance = Classroom.objects.create(whole=time_slot['classroom']['building'] + '-'
                                                                        + time_slot['classroom']['room_no'],
                                                                  building=time_slot['classroom']['building'],
                                                                  room_no=time_slot['classroom']['room_no'])
                    classroom_instance.save()

                timeslot_instance = TimeSlot.objects.create(day_of_week=time_slot['time'][0],
                                                            start_time=time_slot['time'][2:7],
                                                            end_time=time_slot['time'][8:13],
                                                            classroom=classroom_instance)

                timeslot_instance.save()
                lecture_instance.time_slots.add(timeslot_instance)

        except Exception as e:
            print(e)
