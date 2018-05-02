"""
IMPORTANT: It is a mock crawler.

function run is called by view with argument crawler.
while crawling the site, it updates status of the crawler and
checks cancel_flag of it.
If cancel_flag is True, it stops current job and set status to 'canceled'.
"""

from django.core.exceptions import ObjectDoesNotExist


def run(crawler):
    # let # of total lectures is 1200
    total_cnt = 1200

    try:
        for i in range(total_cnt):
            # refresh crawler dynamically
            crawler.refresh_from_db()
            if crawler.cancel_flag:
                # administrator canceled this crawler
                crawler.status = 'canceled {}/{}'.format(i, total_cnt)
                crawler.save()
                return

            # for the test, sleep a little
            # in product, there will be a several tasks for scraping data
            import time
            time.sleep(0.015)

            # change status of crawler and save
            crawler.refresh_from_db()
            crawler.status = 'running {}/{}'.format(i, total_cnt)
            crawler.save()

        # finish crawling
        crawler.status = 'finished {}'.format(total_cnt)
        crawler.save()

    except ObjectDoesNotExist as e:
        print(e)
    except Exception as e:
        crawler.status = str(e)
        crawler.save()
