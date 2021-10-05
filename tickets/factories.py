import datetime

import factory
from django.contrib.auth.models import User
from factory import Faker
from faker import Factory

from tickets.models import Ticket


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    first_name = Faker('name')
    username = factory.LazyFunction(Factory.create().name)
    password = Faker('password')


# list of possible ticket statuses
statuses = ['Open', 'Closed', 'Frozen']


class TicketFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Ticket

    title = Faker('sentence', nb_words=4)
    description = Faker('text')
    status = Faker('word', ext_word_list=statuses)
    user = factory.SubFactory(UserFactory)
    creation_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
