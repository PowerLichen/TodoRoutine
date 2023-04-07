from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from api.routine.renderers import RoutineJSONRenderer
from lib.factory.client_factory import ClientDataFactory
from lib.factory.routine_factory import RoutineFactory
from lib.factory.routine_factory import RoutineDayFactory
from model.routine.models import Routine


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
        cls.success_msg = RoutineJSONRenderer.routine_msgs["destroy"]
        
    def test_routine_delete_by_anonymous(self):
        """익명 유저 루틴 삭제 테스트"""
        res = self.client.delete(
            self.url
        )
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_routine_delete_success(self):
        """루틴 삭제 성공 테스트"""
        res = self.auth_client.client.delete(
            self.url
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["message"]["msg"], self.success_msg["msg"])
        self.assertEqual(res.data["message"]["status"], self.success_msg["status"])
        
        routine_id = res.data["data"]["routine_id"]
        instance = Routine.objects.get(routine_id=routine_id)
        self.assertEqual(instance.is_deleted, True)
        
        result_set = instance.routine_result_set.all()
        for result in result_set:
            self.assertEqual(result.is_deleted, True)
            
