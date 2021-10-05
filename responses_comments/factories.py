import datetime
import factory
from factory import Faker

from authentication.factories import UserFactory
from responses_comments.models import Response
from tickets.factories import TicketFactory


class ResponseFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Response

    initial_ticket = factory.SubFactory(TicketFactory)
    content = Faker('text')
    support_member = factory.SubFactory(UserFactory)
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
