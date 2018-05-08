from django.db import models


class Crawler(models.Model):
    started = models.DateTimeField(auto_now_add=True)
    year = models.CharField(max_length=10)
    semester = models.CharField(max_length=10)
    status = models.TextField()
    cancel_flag = models.BooleanField(default=False)

    def __str__(self):
        return '{}-{} {}'.format(self.year, self.semester, self.status)
