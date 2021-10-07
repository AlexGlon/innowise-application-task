from django.db import models
from django.contrib.auth.models import User

from attachments.models import Attachment


class Ticket(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    attachments = models.ManyToManyField(Attachment, blank=True)
    # TODO: turn into IntegerField?
    status = models.CharField(max_length=15)
    # necessary for 'Close outdated tickets' celery task
    force_closed = models.BooleanField()
    # `related_name` is necessary for UserSerializer to retrieve `tickets` field
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='tickets')
    creation_time = models.DateTimeField()

    def __str__(self):
        return str(self.title)
