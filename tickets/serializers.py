from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        # TODO: right now we have to explicitly declare all fields here because permission hijinks
        # TODO: rework this into using fields = '__all__' w/out breaking the viewset
        fields = ('url', 'username', 'email', 'groups', )
        read_only_field = ('id', )
        # lookup_field = 'username'
