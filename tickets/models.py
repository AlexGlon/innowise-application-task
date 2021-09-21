from django.db import models

# Create your models here.


class Ticket(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    status = models.CharField()
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
    initial_reply_id = models.IntegerField(null=True)
    reply = models.TextField()
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    time = models.DateTimeField()

    def __str__(self):
        return str(self.id)
