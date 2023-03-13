from freezegun import freeze_time
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from api.routine.renderers import RoutineJSONRenderer
from lib.factory.client_factory import ClientDataFactory
from lib.factory.routine_factory import RoutineFactory
from lib.factory.routine_factory import RoutineDayFactory

class RoutineResultUpdateTestCase(APITestCase):
    @classmethod
    @freeze_time("2023-02-20")
    def setUpTestData(cls):
        cls.auth_client = ClientDataFactory()
        
        cls.routine = RoutineFactory(
            account=cls.auth_client.user
        )
        RoutineDayFactory(
            day="MON",
            routine=cls.routine
        )
        
        cls.url = reverse(
            "routine-result",
            kwargs={"pk": cls.routine.routine_id},
        )
        cls.success_msg = RoutineJSONRenderer.routine_msgs["result"]
        
    def setUp(self):
        self.auth_client.set_client_auth()
        self.data = {
            "today": "2023-02-20",
            "result": "DONE"
        }
        
    def test_routine_result_update_by_anonymous(self):
        """익명 유저 루틴 수정 권한 테스트"""
        res = self.client.post(
            self.url,
            data=self.data
        )
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)        
        
    def test_routine_result_update_success(self):
        """루틴 결과 수정 성공 테스트"""
        res = self.auth_client.client.post(
            self.url,
            data=self.data
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["message"]["msg"], self.success_msg["msg"])
        self.assertEqual(res.data["message"]["status"], self.success_msg["status"])
        
        instance = self.routine.routine_result_set.filter(created_at__date=self.data["today"]).first()
        self.assertEqual(instance.result, self.data["result"])
        
    def test_routine_result_update_with_today_not_in_routine_days(self):
        """루틴 결과 수정 테스트 (루틴 days에 해당하지 않은 today)"""
        self.data["today"] = "2023-02-21"
        res = self.auth_client.client.post(
            self.url,
            data=self.data
        )
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_routine_result_update_with_invalid_result(self):
        """루틴 결과 수정 테스트 (유효하지 않은 result)"""
        self.data["result"] = "TEST"
        res = self.auth_client.client.post(
            self.url,
            data=self.data
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_routine_result_update_with_missing_today(self):
        """루틴 결과 수정 테스트 (today 누락)"""
        self.data.pop("today")
        res = self.auth_client.client.post(
            self.url,
            data=self.data
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_routine_result_update_with_missing_result(self):
        """루틴 결과 수정 테스트 (result 누락)"""
        self.data.pop("result")
        res = self.auth_client.client.post(
            self.url,
            data=self.data
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
