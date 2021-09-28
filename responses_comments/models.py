from django.db import models
from django.contrib.auth.models import User

from attachments.models import Attachment
from tickets.models import Ticket


class Response(models.Model):
    initial_ticket = models.ForeignKey(Ticket, on_delete=models.DO_NOTHING)
    content = models.TextField()
    support_member = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    time = models.DateTimeField()

    def __str__(self):
        return str(self.id)


class Comment(models.Model):
    initial_response = models.ForeignKey(Response, on_delete=models.DO_NOTHING)
    initial_comment = models.IntegerField(null=True, blank=True)
    content = models.TextField()
    attachments = models.ManyToManyField(Attachment, blank=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    time = models.DateTimeField()

    def __str__(self):
        return str(self.id)
