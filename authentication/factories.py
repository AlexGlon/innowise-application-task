import factory
from django.contrib.auth.models import User
from factory import Faker
from faker import Factory


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    first_name = Faker('name')
    username = factory.LazyFunction(Factory.create().name)
    password = Faker('password')
