from rest_framework import viewsets

from responses_comments.models import Comment, Response
from responses_comments.serializers import CommentSerializer, ResponseSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class ResponseViewSet(viewsets.ModelViewSet):
    queryset = Response.objects.all()
    serializer_class = ResponseSerializer
