from rest_framework import serializers

from responses_comments.models import Comment, Response


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
