from django.db import models
from accounts.models import User
from django.utils.timezone import now


# Create your models here.


class DiscussionGroups(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    disc_title = models.CharField(max_length=255)
    disc_description = models.CharField(max_length=2255)
    date_added = models.DateTimeField(default=now)

    def __str__(self):
        return f'{self.user_id.lname} - {self.disc_title}'
    

class DiscussionReplies(models.Model):
    user_id  = models.ForeignKey(User, on_delete=models.CASCADE)
    discussion_id  = models.ForeignKey(DiscussionGroups, on_delete=models.CASCADE)
    comment = models.CharField(max_length=2255)
    date_added = models.DateTimeField(default=now)

    def __str__(self):
        return f'Comment by:{self.user_id.lname} - Title: {self.discussion_id.disc_title}'

