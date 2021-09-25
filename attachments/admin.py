from django.contrib import admin

from attachments.models import Attachment


@admin.register(Attachment)
class Attachment(admin.ModelAdmin):
    fields = ('image', )
