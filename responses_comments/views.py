from rest_framework import viewsets, status, mixins
from rest_framework.response import Response as APIResponse

from responses_comments.models import Comment, Response
from responses_comments.serializers import CommentSerializer, ResponseSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class ResponseViewSet(viewsets.ModelViewSet):
    queryset = Response.objects.all()
    serializer_class = ResponseSerializer


class CommentsThreadView(mixins.ListModelMixin, viewsets.GenericViewSet):
    """Loads whole comments thread to the specified support response."""
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(initial_response=self.kwargs['pk'])

    def get(self, request, *args, **kwargs):
        comments = self.get_queryset()
        if not comments:
            return APIResponse(status=status.HTTP_204_NO_CONTENT)

        serializer = self.get_serializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ResponseByTicketView(mixins.ListModelMixin, viewsets.GenericViewSet):
    """Loads support response to the specified ticket."""
    serializer_class = ResponseSerializer

    def get_queryset(self):
        return Response.objects.filter(initial_ticket=self.kwargs['ticket_id'])

    def get(self, request, *args, **kwargs):
        tickets = self.get_queryset()
        if not tickets:
            return Response(status=status.HTTP_204_NO_CONTENT)

        serializer = self.get_serializer(tickets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
