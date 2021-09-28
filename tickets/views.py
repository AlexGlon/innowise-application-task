from django.contrib.auth.models import User
from rest_framework import mixins, permissions, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from tickets.serializers import TicketSerializer, UserSerializer
from tickets.models import Ticket


# TODO: remove later
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # TODO: is this necessary?
    # permission_classes = [permissions.IsAuthenticated]


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    @action(methods=['GET'], detail=False, url_path='by_user/(?P<user>[^/.]+)')
    def tickets_by_user(self, request, user):
        """Returns all tickets created by a user with specified ID."""
        # TODO: rewrite this using filter (that'd be defined after serializer_class)?
        tickets = Ticket.objects.filter(user=user)
        if not tickets:
            return Response(status=status.HTTP_204_NO_CONTENT)

        serializer = self.get_serializer(tickets, many=True)
        return Response(serializer.data)

    @action(methods=['GET'], detail=False, url_path='by_status/(?P<ticket_status>[^/.]+)')
    def tickets_by_status(self, request, ticket_status):
        """Returns all tickets that have the specified status."""
        tickets = Ticket.objects.filter(status=ticket_status)
        if not tickets:
            return Response(status=status.HTTP_204_NO_CONTENT)

        serializer = self.get_serializer(tickets, many=True)
        return Response(serializer.data)

    @action(methods=['GET'], detail=False, url_path='by_support_member/(?P<support>[^/.]+)')
    def tickets_by_support_member(self, request, support):
        """Returns all tickets that have been responded to by the specified support member."""
        tickets = Ticket.objects.filter(response__support_member=support)
        if not tickets:
            return Response(status=status.HTTP_204_NO_CONTENT)

        serializer = self.get_serializer(tickets, many=True)
        return Response(serializer.data)

    @action(methods=['PATCH'], detail=True)
    def status_update(self, request, pk=None):
        """Updates status of the selected ticket. Receives a `{"status": "foobar"}` JSON as a request."""
        ticket = self.get_object()

        # `partial=True` allows custom {"status": "foobar"} JSONs to be used
        # `context={'request': request}` is required by `HyperlinkedIdentityField`
        serializer = self.get_serializer(ticket, context={'request': request},
                                      data=request.data, partial=True)
        if serializer.is_valid():
            serializer.validated_data['status'] = request.data['status']
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# TODO: implement status check logic (e.g. user can't comment on a closed ticket)
# TODO: permissions on every ticket
# TODO:
# TODO:
# TODO:
# TODO:
# TODO:
# TODO:
# TODO:
# TODO:
# TODO:
# TODO: remove empty TODOs
