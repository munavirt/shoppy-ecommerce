from django.db import models
from django.utils import timezone
from timeago import format

class ContactUs(models.Model):

    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField(default='hey boii')
    sent_time = models.DateTimeField(auto_now_add=True)
    def time_ago(self):
        now = timezone.now()
        time_diff = format(self.sent_time,now)
        return time_diff

    def __str__(self):
        return self.name