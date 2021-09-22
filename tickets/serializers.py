from django.contrib.auth.models import User
from rest_framework import serializers
from tickets.models import Attachment, Response, Comment, Ticket


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        # TODO: right now we have to explicitly declare all fields here because permission hijinks
        # TODO: rework this into using fields = '__all__' w/out breaking the viewset
        fields = ('url', 'username', 'email', 'groups', )
        read_only_field = ('id', )
        # TODO: is this necessary?
        # lookup_field = 'username'


class TicketSerializer(serializers.ModelSerializer):
    # url = serializers.HyperlinkedIdentityField(view_name='ticket-detail')

    class Meta:
        model = Ticket
        fields = ('url', 'title', 'description', 'attachments', 'status', 'user', 'creation_time', )
        read_only_field = ('id',)


class ResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Response
        fields = ('initial_ticket', 'content', 'support_member', 'time', )
        read_only_field = ('id',)


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('initial_response', 'initial_comment', 'content', 'attachments', 'user', 'time', )
        read_only_field = ('id',)


class AttachmentSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='attachment-detail')

    class Meta:
        model = Attachment
        fields = ('url', 'image', )
        read_only_field = ('id', )
