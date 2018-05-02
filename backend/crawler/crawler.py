# It is a mock crawler.

import time


def run(crawler):
    # let # of total lectures is 1200
    total_cnt = 1200
    for i in range(total_cnt):
        # administrator canceled this crawler
        if crawler.cancel_flag:
            crawler.status = 'canceled'
            crawler.save()
            return

        # for the test, sleep a little
        # in product, there is a several tasks for scraping data
        time.sleep(0.015)

        # change status of crawler and save
        crawler.status = 'running ({}) {}%'.format(total_cnt, i*100//1200)
        crawler.save()

    # finish crawling
    crawler.status = 'finished ({})'.format(total_cnt)
    crawler.save()
