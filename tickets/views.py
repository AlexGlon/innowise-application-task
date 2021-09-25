from django.contrib.auth.models import User
from rest_framework import permissions, viewsets
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
# TODO:
