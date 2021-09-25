from rest_framework import serializers

from attachments.models import Attachment


class AttachmentSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='attachment-detail')

    class Meta:
        model = Attachment
        fields = ('url', 'image', )
        read_only_field = ('id', )
