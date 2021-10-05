import datetime
import factory
from factory import Faker

from authentication.factories import UserFactory
from tickets.models import Ticket


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
