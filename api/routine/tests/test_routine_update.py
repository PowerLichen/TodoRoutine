from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from api.routine.renderers import RoutineJSONRenderer
from lib.factory.client_factory import ClientDataFactory
from lib.factory.routine_factory import RoutineFactory
from lib.factory.routine_factory import RoutineDayFactory
from model.routine.models import Routine
from model.routine.models import RoutineDay


class RoutineUpdateTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.auth_client = ClientDataFactory()
        cls.routine = RoutineFactory(
            account=cls.auth_client.user
        )
        cls.routine_day = RoutineDayFactory.create_batch(
            3,
            routine=cls.routine
        )
        cls.url = reverse(
            "routine-detail",
            kwargs={"pk": cls.routine.routine_id}
        )
        cls.success_msg = RoutineJSONRenderer.routine_msgs["partial_update"]

    def setUp(self):
        self.data = {
            "title" : "problem solving",
            "category" : "HOMEWORK",
            "goal": "Increase your problem-solving skills",
            "is_alarm": False,
            "days": ["MON", "WED", "FRI"]
        }
        
    def test_routine_update_by_anonymous(self):
        """익명 유저 루틴 변경"""
        res = self.client.patch(
            self.url,
            data=self.data
        )
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_routine_update_success(self):
        """루틴 수정 성공 테스트"""
        res = self.auth_client.client.patch(
            self.url,
            data = self.data
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
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

    def test_routine_update_with_title(self):
        """루틴 수정 테스트(title만 변경)"""
        res = self.auth_client.client.patch(
            self.url,
            data = {"title": self.data["title"]}
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        
        routine_id = res.data["data"]["routine_id"]
        instance = Routine.objects.get(routine_id=routine_id)
        self.assertEqual(instance.title, self.data["title"])

    def test_routine_update_with_category(self):
        """루틴 수정 테스트(category만 변경)"""
        res = self.auth_client.client.patch(
            self.url,
            data = {"category": self.data["category"]}
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        
        routine_id = res.data["data"]["routine_id"]
        instance = Routine.objects.get(routine_id=routine_id)
        self.assertEqual(instance.category, self.data["category"])

    def test_routine_update_with_goal(self):
        """루틴 수정 테스트(goal만 변경)"""
        res = self.auth_client.client.patch(
            self.url,
            data = {"goal": self.data["goal"]}
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        
        routine_id = res.data["data"]["routine_id"]
        instance = Routine.objects.get(routine_id=routine_id)
        self.assertEqual(instance.goal, self.data["goal"])

    def test_routine_update_with_alarm(self):
        """루틴 수정 테스트(is_alarm만 변경)"""
        res = self.auth_client.client.patch(
            self.url,
            data = {"is_alarm": self.data["is_alarm"]}
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        
        routine_id = res.data["data"]["routine_id"]
        instance = Routine.objects.get(routine_id=routine_id)
        self.assertEqual(instance.is_alarm, self.data["is_alarm"])

    def test_routine_update_with_days(self):
        """루틴 수정 테스트(days만 변경)"""
        res = self.auth_client.client.patch(
            self.url,
            data = {"days": self.data["days"]}
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        
        routine_id = res.data["data"]["routine_id"]
        day_set = RoutineDay.objects.filter(routine_id=routine_id)
        for routineday in day_set:
            self.assertIn(routineday.day, self.data["days"])

    def test_routine_update_with_invalid_id(self):
        """루틴 수정 테스트(유효하지 않은 id)"""
        res = self.auth_client.client.patch(
            reverse("routine-detail", kwargs={"pk": 1000}),
            data = self.data
        )
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_routine_update_with_invalid_category(self):
        """루틴 수정 테스트(유효하지 않은 category)"""
        res = self.auth_client.client.patch(
            self.url,
            data = {"category": "None"}
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_routine_update_with_invalid_days(self):
        """루틴 수정 테스트(유효하지 않은 days)"""
        res = self.auth_client.client.patch(
            self.url,
            data = {"days": ["TUE", "None"]}
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        
    
        