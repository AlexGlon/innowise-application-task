from django.db import models
from django.contrib.auth.models import User


class Attachment(models.Model):
    image = models.ImageField(upload_to='images')

    def __str__(self):
        return str(self.id)


class Ticket(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    attachments = models.ManyToManyField(Attachment, blank=True)
    # TODO: turn into IntegerField?
    status = models.CharField(max_length=15)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    creation_time = models.DateTimeField()

    def __str__(self):
        return str(self.id)


class Comment(models.Model):
    initial_ticket = models.ForeignKey(Ticket, on_delete=models.DO_NOTHING)
    comment = models.TextField()
    support_user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    time = models.DateTimeField()

    def __str__(self):
        return str(self.id)


class Reply(models.Model):
    initial_comment = models.ForeignKey(Comment, on_delete=models.DO_NOTHING)
    initial_reply = models.IntegerField(null=True)
    reply = models.TextField()
    attachments = models.ManyToManyField(Attachment, blank=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    time = models.DateTimeField()

    def __str__(self):
        return str(self.id)
