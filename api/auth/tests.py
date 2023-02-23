from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.test import APITestCase


class AuthTestCore(APITestCase):
    def do_register(self, data):
        res = self.client.post(
            "/api/auth/register/",
            data=data
        )        
        return res
    
    def do_login(self, data):
        res = self.client.post(
            "/api/auth/login/",
            data=data
        )
        return res


class AuthTestCase(AuthTestCore):
    client = APIClient()
    
    def setUp(self):
        self.email = "test@test.com"
        self.password = "aaaa123!"
        self.username = "test_account"
        
        data = {
            "email": self.email,
            "password": self.password,
            "username": self.username
        }
        self.do_register(data)
    
    def test_register_success(self):
        data = {
            "email": "hi@hello.com",
            "password": "aaaa123!",
            "username": "hi",
        }
        
        res = self.do_register(data)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data["email"], data["email"])
        self.assertEqual(res.data["username"], data["username"])
        
    def test_register_email_error(self):
        # missing email
        data = {
            "email": "mail@test.com"
        }
        res = self.do_register(data)
        
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        
        # invalid email
        data = {
            "email": "invalid_mail@",
            "password": self.password
        }
        res = self.do_register(data)
        
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_password_error(self):
        data = {
            "email": "mail@error.com",
            "username": "pwd_err_tester"
        }
        
        # check password length less than 8
        data["password"] = "a"
        res = self.do_register(data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        
        # check password not contain symbols
        data["password"] = "aaaaaaa1"
        res = self.do_register(data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        
        # check password not contain numeric character
        data["password"] = "aaaaaaa!"
        res = self.do_register(data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_login_success(self):
        data = {
            "email": self.email,
            "password": self.password
        }
        res = self.do_login(data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        
    def test_login_error(self):
        salt = "asdf"
        
        # not contain email
        data = {
            "email": self.email + salt,
            "password": self.password
        }
        res = self.do_login(data)
        
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # invalid password
        data = {
            "email": self.email,
            "password": self.password + salt
        }
        res = self.do_login(data)
        
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        
        