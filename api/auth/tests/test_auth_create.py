from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase


class AuthCreateTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse("register")
        
    def setUp(self):
        self.data = {
            "email": "test@example.com",
            "password": "aaaa123!",
            "username": "test"
        }
        
    def test_auth_create_success(self):
        """익명 유저 계정 생성 성공 테스트"""
        res = self.client.post(
            self.url,
            data=self.data
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data["email"], self.data["email"])
        self.assertEqual(res.data["username"], self.data["username"])
        
    def test_auth_create_with_missing_email(self):
        """계정 생성 실패 테스트(email 누락)"""
        self.data.pop("email")
        res = self.client.post(
            self.url,
            data=self.data
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_auth_create_with_missing_password(self):
        """계정 생성 실패 테스트(password 누락)"""
        self.data.pop("password")
        res = self.client.post(
            self.url,
            data=self.data
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_auth_create_with_invalid_email(self):
        """계정 생성 실패 테스트(잘못된 이메일)"""
        self.data["email"] = "testtest@"
        res = self.client.post(
            self.url,
            data=self.data
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_auth_create_with_password_length_less_than_8(self):
        """계정 생성 실패 테스트(password 8자리 이하)"""
        self.data["password"] = "1!"
        res = self.client.post(
            self.url,
            data=self.data
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_auth_create_with_password_not_contain_symbols(self):
        """계정 생성 실패 테스트(password 특수문자 없음)"""
        self.data["password"] = "12345678"
        res = self.client.post(
            self.url,
            data=self.data
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_auth_create_with_password_not_contain_number(self):
        """계정 생성 실패 테스트(password 숫자 없음)"""
        self.data["password"] = "aaaaaaa!"
        res = self.client.post(
            self.url,
            data=self.data
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
