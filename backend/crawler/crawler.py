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


tid = {'교양': 2,
       '전필': 3,
       '전선': 4,
       '일선': 5,
       '교직': 6,
       '논문': 7,
       '대학원': 8,
       '학사': 9,
}

fid = {
    '학문의 기초': 2,
    '학문의 세계': 3,
    '선택교양': 4,
    '전공영역': 5,
}

aid = {
    '학문의 기초': {
        '사고와 표현': 2,
        '외국어': 3,
        '수량적 분석과 추론': 4,
        '과학적 사고와 실험': 5,
        '컴퓨터와 정보 활용': 6,
    },
    '학문의 세계': {
        '언어와 문학': 2,
        '문화와 예술': 3,
        '역사와 철학': 4,
        '정치와 경제': 5,
        '인간과 사회': 6,
        '자연과 기술': 7,
        '생명과 환경': 8,
    },
    '선택교양': {
        '체육': 2,
        '예술 실기': 3,
        '대학과 리더십': 4,
        '창의와 융합': 5,
        '한국의 이해': 6,
    },
    '전공영역': {
        '전체': 1,
    },
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
        # detailed search
        driver.find_element_by_id('detail_button').click()
        driver.implicitly_wait(1)
        # select year
        driver.find_element_by_xpath('//*[@id="srchOpenSchyy"]').clear()
        driver.implicitly_wait(1)
        driver.find_element_by_xpath('//*[@id="srchOpenSchyy"]').send_keys(crawler.year)
        driver.implicitly_wait(1)
        # select semester
        driver.find_element_by_xpath('//*[@id="srchOpenShtm"]/option[{}]'.format(sid[crawler.semester])).click()
        driver.implicitly_wait(1)
        # select bachelor's course
        driver.find_element_by_xpath('//*[@id="srchOpenSubmattCorsFg"]/option[2]').click()
        driver.implicitly_wait(1)

        #driver.find_element_by_class_name('btn_search_ok').click()
        #driver.implicitly_wait(1)

        for type in tid:
            crawl_type(crawler, driver, type)

        #total_cnt = int(driver.find_element_by_xpath('//*[@id="content"]/div/div[3]/div[1]/div[1]/h3/span').text)
        #total_page = ((total_cnt-1)//10)+1

        #for i in range(1, total_page+1):
        #    # refresh crawler dynamically
        #    crawler.refresh_from_db()
        #    if crawler.cancel_flag:
        #        # administrator canceled this crawler
        #        crawler.status = 'canceled {}/{}'.format(i, total_page)
        #        crawler.save()
        #        return
        #
        #    # goes to page i
        #    driver.execute_script('fnGotoPage({})'.format(i))
        #    # crawls a table of lectures in current page
        #    print('=====================page {}====================='.format(i))
        #    lectures = crawl(driver)
        #    # parses given data and saves it in DB
        #    parse(crawler.year, crawler.semester, lectures)
        #
        #    # change status of crawler and save
        #    crawler.refresh_from_db()
        #    crawler.status = 'running {}/{}'.format(i, total_page)
        #    crawler.save()

        # finish crawling
        crawler.status = 'finished {}'.format(total_page)
        crawler.save()

        driver.close()

    except ObjectDoesNotExist as e:
        print(e)

    except Exception as e:
        crawler.status = str(e)
        crawler.save()


def crawl_type(crawler, driver, type):
    driver.find_element_by_xpath('//*[@id="srchOpenSubmattFgCd"]/option[{}]'.format(tid[type])).click()
    driver.implicitly_wait(1)

    if type != '교양':
        driver.find_element_by_class_name('btn_search_ok').click()
        driver.implicitly_wait(1)

        total_cnt = int(driver.find_element_by_xpath('//*[@id="content"]/div/div[3]/div[1]/div[1]/h3/span').text)
        total_page = ((total_cnt-1)//10)+1

        for i in range(1, 3): #total_page+1):
            # refresh crawler dynamically
            crawler.refresh_from_db()
            if crawler.cancel_flag:
                # administrator canceled this crawler
                crawler.status = 'canceled {} {}/{}'.format(type, i, total_page)
                crawler.save()
                return

            # goes to page i
            driver.execute_script('fnGotoPage({})'.format(i))
            # crawls a table of lectures in current page
            print('====================={} page {}====================='.format(type, i))
            lectures = crawl(driver)
            # parses given data and saves it in DB
            parse(crawler.year, crawler.semester, lectures, '')

            # change status of crawler and save
            crawler.refresh_from_db()
            crawler.status = 'running {} {}/{}'.format(type, i, total_page)
            crawler.save()

        print('finished {}'.format(type))

    else:
        for field in fid:
            driver.find_element_by_xpath('//*[@id="srchOpenUpSbjtFldCd"]/option[{}]'.format(fid[field]))
            driver.implicitly_wait(1)
            for area in aid[field]:
                driver.find_element_by_xpath('//*[@id="cond02"]/td[3]/select[2]/option[{}]'.format(aid[field][area]))
                driver.implicitly_wait(1)

                driver.find_element_by_class_name('btn_search_ok').click()
                driver.implicitly_wait(1)

                total_cnt = int(driver.find_element_by_xpath('//*[@id="content"]/div/div[3]/div[1]/div[1]/h3/span').text)
                total_page = ((total_cnt - 1) // 10) + 1

                for i in range(1, 3):  # total_page+1):
                    # refresh crawler dynamically
                    crawler.refresh_from_db()
                    if crawler.cancel_flag:
                        # administrator canceled this crawler
                        crawler.status = 'canceled {} ({}-{}) {}/{}'.format(type, field, area, i, total_page)
                        crawler.save()
                        return

                    # goes to page i
                    driver.execute_script('fnGotoPage({})'.format(i))
                    # crawls a table of lectures in current page
                    print('====================={} ({}-{}) page {}====================='.format(type, field, area, i))
                    lectures = crawl(driver)
                    # parses given data and saves it in DB
                    parse(crawler.year, crawler.semester, lectures, field + '-' + area)

                    # change status of crawler and save
                    crawler.refresh_from_db()
                    crawler.status = 'running {} ({}-{}) {}/{}'.format(type, field, area, i, total_page)
                    crawler.save()

                print('finished {} ({}-{})'.format(type, field, area))
        pass




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

                department_major = columns[3].text
                if department_major != '':
                    if department_major[0] == '(':
                        department_major = department_major[1:]

                    if department_major[-1] == ')':
                        department_major = department_major[:-1]

                    index = department_major.find('(')
                    if index != -1:
                        department = department_major[:index]
                        major = department_major[index+1:]
                    else:
                        department = department_major
                        major = ''
                else:
                    department = ''
                    major = ''

                #print('lecture:', columns[8].text, 'department:', department, 'major:', major)

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
                    'note': columns[17].text,
                }

                if not columns[10].text:
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

                elif len(classroom) == 2:
                    building = classroom[0]
                    room_no = classroom[1]

                else:
                    building = classroom[0]
                    room_no = ''

                time_slot = {
                    'time': columns[10].text,
                    'classroom': {
                        'building': building,
                        'room_no': room_no,
                    }
                }

                lecture['time_slots'] = [time_slot]

            else:
                if not columns[0].text:
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

                elif len(classroom) == 2:
                    building = classroom[0]
                    room_no = classroom[1]

                else:
                    building = classroom[0]
                    room_no = ''

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


def parse(year, semester, lectures, field_name):
    for lecture in lectures:
        try:
            college_instance = College.objects.get(name=lecture['college'])
        except ObjectDoesNotExist:
            college_instance = College.objects.create(name=lecture['college'])
            college_instance.save()

        try:
            department_instance = Department.objects.get(name=lecture['department'])
        except ObjectDoesNotExist:
            if lecture['department'] != '':
                department_instance = Department.objects.create(college=college_instance,
                                                            name=lecture['department'])
                department_instance.save()

            else:
                department_instance = None

        try:
            major_instance = Major.objects.get(name=lecture['major'])
        except ObjectDoesNotExist:
            if lecture['major'] != '':
                major_instance = Major.objects.create(department=department_instance,
                                                  name=lecture['major'])
                major_instance.save()

            else:
                major_instance = None

        try:
            course_instance = Course.objects.get(code=lecture['code'])

        except ObjectDoesNotExist:
            course_instance = Course.objects.create(code=lecture['code'],
                                                    name=lecture['name'],
                                                    type=lecture['type'],
                                                    field=field_name,
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
                                                  note=lecture['note'])

        # It really is absurd, but there exists lectures without any time slot.
        try:
            for time_slot in lecture['time_slots']:
                building = time_slot['classroom']['building']
                room_no = time_slot['classroom']['room_no']

                try:
                    classroom_instance = Classroom.objects.get(building=building, room_no=room_no)
                except ObjectDoesNotExist:
                    if building != '' or room_no != '':
                        classroom_instance = Classroom.objects.create(building=building,
                                                                      room_no=room_no)
                        classroom_instance.save()
                    else:
                        classroom_instance = None

                timeslot_instance = TimeSlot.objects.create(day_of_week=time_slot['time'][0],
                                                            start_time=time_slot['time'][2:7],
                                                            end_time=time_slot['time'][8:13],
                                                            classroom=classroom_instance)
                timeslot_instance.save()
                lecture_instance.time_slots.add(timeslot_instance)

        except Exception as e:
            print('parse', e)
