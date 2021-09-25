from django.contrib.auth.models import User
from rest_framework import serializers

from tickets.models import Ticket


# TODO: remove later?
class UserSerializer(serializers.ModelSerializer):
    tickets = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        # TODO: right now we have to explicitly declare all fields here because permission hijinks
        # TODO: rework this into using fields = '__all__' w/out breaking the viewset
        fields = ('id', 'url', 'username', 'email', 'groups', 'tickets', )
        # TODO: is this necessary?
        # lookup_field = 'username'


class TicketSerializer(serializers.ModelSerializer):
    # url = serializers.HyperlinkedIdentityField(view_name='ticket-detail')

    class Meta:
        model = Ticket
        fields = ('url', 'title', 'description', 'attachments', 'status', 'user', 'creation_time', )
        read_only_field = ('id',)
