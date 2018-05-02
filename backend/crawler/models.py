from django.db import models


class Crawler(models.Model):
    started = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20)
    cancel_flag = models.BooleanField(default=False)

    def __str__(self):
        return 'Crawler {} - {}'.format(self.id, self.status)
