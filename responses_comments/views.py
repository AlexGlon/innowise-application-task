from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response as APIResponse

from responses_comments.models import Comment, Response
from responses_comments.serializers import CommentSerializer, ResponseSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class ResponseViewSet(viewsets.ModelViewSet):
    queryset = Response.objects.all()
    serializer_class = ResponseSerializer

    # TODO: move to CommentViewSet?
    @action(methods=['GET'], detail=True)
    def load_comments(self, request, pk):
        """Loads whole comments thread to the specified support response."""
        comments = Comment.objects.filter(initial_response=pk)
        if not comments:
            return APIResponse(status=status.HTTP_204_NO_CONTENT)

        serializer = CommentSerializer(comments, many=True).data
        return APIResponse(serializer)

    @action(methods=['GET'], detail=False, url_path='by_ticket/(?P<ticket_id>[^/.]+)')
    def load_response_by_ticket(self, request, ticket_id):
        """Loads support response to the specified ticket."""
        response = Response.objects.get(initial_ticket=ticket_id)
        if not response:
            return APIResponse(status=status.HTTP_204_NO_CONTENT)

        serializer = self.get_serializer(response)
        return APIResponse(serializer.data)
