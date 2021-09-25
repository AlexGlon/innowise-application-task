from django.contrib import admin

from responses_comments.models import Comment, Response


@admin.register(Response)
class Response(admin.ModelAdmin):
    fields = ('initial_ticket', 'content', 'support_member', 'time', )


@admin.register(Comment)
class Comment(admin.ModelAdmin):
    fields = ('initial_response', 'initial_comment', 'content', 'attachments', 'user', 'time', )
