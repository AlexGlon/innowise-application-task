from rest_framework import serializers

from attachments.models import Attachment


class AttachmentSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='attachment-detail')

    class Meta:
        model = Attachment
        fields = ('id', 'url', 'image', )
        read_only_field = ('id', )
