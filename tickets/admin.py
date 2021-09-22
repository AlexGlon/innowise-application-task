from django.contrib import admin
from tickets.models import Attachment, Response, Comment, Ticket


@admin.register(Attachment)
class Attachment(admin.ModelAdmin):
    fields = ('image', )


@admin.register(Response)
class Response(admin.ModelAdmin):
    fields = ('initial_ticket', 'content', 'support_member', 'time', )


@admin.register(Comment)
class Comment(admin.ModelAdmin):
    fields = ('initial_response', 'initial_comment', 'content', 'attachments', 'user', 'time', )


@admin.register(Ticket)
class Ticket(admin.ModelAdmin):
    fields = ('title', 'description', 'attachments', 'status', 'user', 'creation_time', )
