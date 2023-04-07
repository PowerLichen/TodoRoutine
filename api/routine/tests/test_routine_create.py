from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from api.routine.renderers import RoutineJSONRenderer
from lib.factory.client_factory import ClientDataFactory
from model.routine.models import Routine


class RoutineCreateTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.auth_client = ClientDataFactory()
        cls.url = reverse("routine-list")
        cls.success_msg = RoutineJSONRenderer.routine_msgs["create"]
        
    def setUp(self):
        self.data = {
            "title" : "problem solving",
            "category" : "HOMEWORK",
            "goal": "Increase your problem-solving skills",
            "is_alarm": True,
            "days": ["MON", "WED", "FRI"]
        }
        
    def test_routine_create_success(self):
        """루틴 생성 성공 테스트"""
        res = self.auth_client.client.post(
            self.url,
            data=self.data
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data["message"]["msg"], self.success_msg["msg"])
        self.assertEqual(res.data["message"]["status"], self.success_msg["status"])
        
        routine_id = res.data["data"]["routine_id"]
        instance = Routine.objects.get(routine_id=routine_id)
        self.assertEqual(instance.title, self.data["title"])
        self.assertEqual(instance.category, self.data["category"])
        self.assertEqual(instance.goal, self.data["goal"])
        self.assertEqual(instance.is_alarm, self.data["is_alarm"])
        
        day_set = instance.routine_day_set.all()
        for routineday in day_set:
            self.assertIn(routineday.day, self.data["days"])

    def test_routine_create_with_missing_title(self):
        """루틴 생성 실패 테스트 (title 누락)"""
        self.data.pop("title")
        res = self.auth_client.client.post(
            self.url,
            data=self.data
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_routine_create_with_missing_category(self):
        """루틴 생성 실패 테스트 (category 누락)"""
        self.data.pop("category")
        res = self.auth_client.client.post(
            self.url,
            data=self.data
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_routine_create_with_missing_goal(self):
        """루틴 생성 실패 테스트 (goal 누락)"""
        self.data.pop("goal")
        res = self.auth_client.client.post(
            self.url,
            data=self.data
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_routine_create_with_missing_days(self):
        """루틴 생성 실패 테스트 (days 누락)"""
        self.data.pop("days")
        res = self.auth_client.client.post(
            self.url,
            data=self.data
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_routine_create_with_invalid_category(self):
        """루틴 생성 실패 테스트 (잘못된 카테고리)"""
        self.data["category"] = "TEST"
        res = self.auth_client.client.post(
            self.url,
            data=self.data
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_routine_create_with_invalid_days(self):
        """루틴 생성 실패 테스트 (잘못된 요일이름)"""
        self.data["days"] = ["MON", "TEST"]
        res = self.auth_client.client.post(
            self.url,
            data=self.data
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
