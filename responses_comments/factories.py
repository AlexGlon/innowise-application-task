import datetime
import random

import factory
from factory import Faker

from authentication.factories import UserFactory
from responses_comments.models import Comment, Response
from tickets.factories import TicketFactory


class ResponseFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Response

    initial_ticket = factory.SubFactory(TicketFactory)
    content = Faker('text')
    support_member = factory.SubFactory(UserFactory)
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Comment

    initial_response = factory.SubFactory(ResponseFactory)
    # TODO: reimplement this
    initial_comment = random.randrange(1, 15)
    content = Faker('text')
    user = factory.SubFactory(UserFactory)
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
