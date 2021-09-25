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

    @action(methods=['GET'], detail=False, url_path='tickets_by_user/(?P<user>[^/.]+)')
    def tickets_by_user(self, request, user):
        # TODO: rewrite this using filter (that'd be defined after serializer_class)?
        tickets = Ticket.objects.filter(user=user)
        if not tickets:
            return Response(status=status.HTTP_204_NO_CONTENT)

        serializer = self.get_serializer(tickets, many=True)
        return Response(serializer.data)


# TODO: a view that lets a user check all his tickets
# TODO: a view that lets support members check tickets by category
# TODO: update method on tickets that lets support members change their status
# TODO: implement status check logic (e.g. user can't comment on a closed ticket)
# TODO:
# TODO:
# TODO:
# TODO:
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
