import factory
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from lib.factory.user_factory import UserFactory


class ClientData:
    def __init__(self, email):
        self.user = UserFactory(
            email=email
        )
        self.email = email
        self.set_client_auth()
        
    def set_client_auth(self):
        refresh = RefreshToken.for_user(user=self.user)
        access = refresh.access_token
        self.client = APIClient()
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {access}"
        )


class ClientDataFactory(factory.Factory):
    class Meta:
        model = ClientData
        
    email = factory.Faker("safe_email")