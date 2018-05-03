import os
from django.conf import settings

driver_path = os.path.join(settings.BASE_DIR, '../chromedriver')

from django.core.exceptions import ObjectDoesNotExist
from selenium import webdriver

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

semester = '1학기'


def run(crawler):
    print(settings.BASE_DIR)
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument('disable-gpu')
    options.add_argument('User-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KTHML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')


    driver = webdriver.Chrome(driver_path, chrome_options=options)
    driver.implicitly_wait(3)

    driver.get('https://sugang.snu.ac.kr/sugang/cc/cc100.action')
    driver.find_element_by_id('detail_button').click()
    driver.find_element_by_xpath('//*[@id="srchOpenShtm"]/option[{}]'.format(sid[semester])).click()
    driver.find_element_by_xpath('//*[@id="srchOpenSubmattCorsFg"]/option[2]').click()
    driver.find_element_by_class_name('btn_search_ok').click()

    total_cnt = int(driver.find_element_by_xpath('//*[@id="content"]/div/div[3]/div[1]/div[1]/h3/span').text)
    total_page = ((total_cnt-1) // 10) + 1

    try:
        for i in range(1, total_page + 1):
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
            parse(lectures)

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
                    # print(i, lecture)
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

    return lectures


def parse(lectures):
    for lecture in lectures:
        try:
            college_instance = College.objects.get(name=lecture['college'])
        except Exception as e:
            college_instance = College.objects.create(name=lecture['college'])
            college_instance.save()

        try:
            department_instance = Department.objects.get(name=lecture['department'])
        except Exception as e:
            department_instance = Department.objects.create(college=college_instance,
                                                   name=lecture['department'])
            department_instance.save()

        course_instance = Course.objects.create(code=lecture['code'],
                                                name=lecture['name'],
                                                type=lecture['type'],
                                                # field=,
                                                grade=int(lecture['grade'][0]),
                                                credit=int(lecture['credit'].split('-')[0]),
                                                college=college_instance,
                                                department=department_instance,
                                                # major=
                                                )
        course_instance.save()

        lecture_instance = Lecture.objects.create(course=course_instance,
                                                  year=2018,
                                                  semester=lecture['semester'],
                                                  number=lecture['number'],
                                                  instructor=lecture['instructor'],
                                                  note='')

        # It really is absurd, but there exists lectures without any time slot.
        try:
            for time_slot in lecture['time_slots']:
                classroom_instance = Classroom.objects.create(building=time_slot['classroom']['building'],
                                                              room_no=time_slot['classroom']['room_no'])
                classroom_instance.save()

                timeslot_instance = TimeSlot.objects.create(start=day[time_slot['time'][0]] + time_slot['time'][2:7] + 'Z',
                                                            end=day[time_slot['time'][0]] + time_slot['time'][8:13] + 'Z',
                                                            classroom=cr)
                timeslot_instance.save()
                lecture_instance.time_slots.add(timeslot_instance)

        except Exception as e:
            print(e)
