import factory
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from lib.factory.user_factory import UserFactory


class ClientData:
    def __init__(self, email):
        user = UserFactory(
            email=email
        )
        self.email = email
        self.client = self._get_client(user)
        
    def _get_client(self, user):
        refresh = RefreshToken.for_user(user=user)
        access = refresh.access_token
        client = APIClient()
        client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {access}"
        )        
        return client


class ClientDataFactory(factory.Factory):
    class Meta:
        model = ClientData
        
    email = factory.Faker("safe_email")