import factory
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserModel
    
    email = factory.Faker("safe_email")
    password = factory.Faker("password")
    username = factory.Faker("user_name")
