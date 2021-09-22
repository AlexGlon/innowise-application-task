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


class Response(models.Model):
    initial_ticket = models.ForeignKey(Ticket, on_delete=models.DO_NOTHING)
    content = models.TextField()
    support_member = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    time = models.DateTimeField()

    def __str__(self):
        return str(self.id)


class Comment(models.Model):
    initial_response = models.ForeignKey(Response, on_delete=models.DO_NOTHING)
    initial_comment = models.IntegerField(null=True)
    content = models.TextField()
    attachments = models.ManyToManyField(Attachment, blank=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    time = models.DateTimeField()

    def __str__(self):
        return str(self.id)
