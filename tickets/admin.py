from django.contrib import admin
from tickets.models import Attachment, Comment, Reply, Ticket


@admin.register(Attachment)
class Attachment(admin.ModelAdmin):
    fields = ('image', )


@admin.register(Comment)
class Comment(admin.ModelAdmin):
    fields = ('initial_ticket', 'comment', 'support_member', 'time', )


@admin.register(Reply)
class Reply(admin.ModelAdmin):
    fields = ('initial_comment', 'initial_reply', 'reply', 'attachments', 'user', 'time', )


@admin.register(Ticket)
class Ticket(admin.ModelAdmin):
    fields = ('title', 'description', 'attachments', 'status', 'user', 'creation_time', )
