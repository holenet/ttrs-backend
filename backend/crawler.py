from selenium import webdriver
from selenium.webdriver.support.ui import Select

driver = webdriver.Chrome('/home/newlame/PycharmProjects/untitled/chromedriver')
driver.implicitly_wait(3)

driver.get('https://sugang.snu.ac.kr/sugang/cc/cc100.action')
driver.find_element_by_id('detail_button').click()
driver.find_element_by_xpath('//*[@id="srchOpenShtm"]/option[3]').click()
driver.find_element_by_xpath('//*[@id="srchOpenSubmattCorsFg"]/option[2]').click()
#driver.find_element_by_id('srchSbjtCd').send_keys('')
#driver.find_element_by_id('srchSbjtNm').send_keys('')
driver.find_element_by_class_name('btn_search_ok').click()

page_end = int(driver.find_element_by_xpath('//*[@id="content"]/div/div[3]/div[1]/div[1]/h3/span').text)//10 + 1

lectures = []
errors = []

for i in range(1, page_end):
    driver.execute_script('fnGotoPage({})'.format(i))
    elts = driver.find_element_by_xpath('//*[@id="content"]/div/div[3]/div[1]/div[2]/table/tbody')
    lecture = None
    for row in elts.find_elements_by_tag_name('tr'):
        try:
            columns = row.find_elements_by_tag_name('td')
            if not columns[0].text:
                if lecture is not None:
                    lectures.append(lecture)
                    print(i, lecture)
                lecture = {
                    'type': columns[1].text,
                    'course_name': columns[8].text,
                    'department': columns[3].text,
                    'college': columns[2].text,
                    'grade': columns[5].text,
                    'instructor': columns[13].text,
                    'lecture_code': columns[6].text,
                    'lecture_no': columns[7].text,
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

                lecture['time_slots'] = []
                lecture['time_slots'].append(time_slot)

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

print(errors)
driver.close()