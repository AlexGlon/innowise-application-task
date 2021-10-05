from django.contrib.auth.models import User
from rest_framework import mixins, permissions, viewsets, status, generics
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


class TicketsByUserView(mixins.ListModelMixin, viewsets.GenericViewSet):
    """Returns all tickets created by a user with specified ID."""
    serializer_class = TicketSerializer

    def get_queryset(self):
        return Ticket.objects.filter(user=self.kwargs['user'])

    def get(self, request, *args, **kwargs):
        tickets = self.get_queryset()
        if not tickets:
            return Response(status=status.HTTP_204_NO_CONTENT)

        serializer = self.get_serializer(tickets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TicketsByStatusView(mixins.ListModelMixin, viewsets.GenericViewSet):
    """Returns all tickets that have the specified status."""
    serializer_class = TicketSerializer

    def get_queryset(self):
        return Ticket.objects.filter(status=self.kwargs['ticket_status'])

    def get(self, request, *args, **kwargs):
        tickets = self.get_queryset()
        if not tickets:
            return Response(status=status.HTTP_204_NO_CONTENT)

        serializer = self.get_serializer(tickets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TicketsBySupportMemberView(mixins.ListModelMixin, viewsets.GenericViewSet):
    """Returns all tickets that have been responded to by the specified support member."""
    serializer_class = TicketSerializer

    def get_queryset(self):
        return Ticket.objects.filter(response__support_member=self.kwargs['support'])

    def get(self, request, *args, **kwargs):
        tickets = self.get_queryset()
        if not tickets:
            return Response(status=status.HTTP_204_NO_CONTENT)

        serializer = self.get_serializer(tickets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TicketStatusUpdateView(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """Updates status of the selected ticket. Receives a `{"status": "foobar"}` JSON as a request."""
    # necessary as otherwise this view won't work at all
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    # def get_queryset(self):
    #     # TODO: it'd be better if `objects.get` method was used here, but using it throws an exception
    #     return Ticket.objects.get(id=self.kwargs['pk'])

    def put(self, request, *args, **kwargs):
        ticket = Ticket.objects.get(id=self.kwargs['pk'])

        # `partial=True` allows custom {"status": "foobar"} JSONs to be used
        serializer = self.get_serializer(ticket, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.validated_data['status'] = request.data['status']
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# TODO: implement status check logic (e.g. user can't comment on a closed ticket)
# TODO: permissions on every ticket
# TODO: TESTS TESTS TESTS TESTS TESTS TESTS
# TODO: authentication
# TODO:
# TODO:
# TODO:
# TODO:
# TODO:
# TODO:
# TODO:
# TODO: remove empty TODOs
