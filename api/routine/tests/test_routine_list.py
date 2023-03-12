from freezegun import freeze_time
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from api.routine.renderers import RoutineJSONRenderer
from lib.factory.client_factory import ClientDataFactory
from lib.factory.routine_factory import RoutineFactory
from lib.factory.routine_factory import RoutineDayFactory
from lib.factory.routine_factory import RoutineResultFactory
from model.routine.models import RoutineResult


class RoutineListTestCase(APITestCase):
    @classmethod
    @freeze_time("2023-02-20")
    def setUpTestData(cls):
        cls.auth_client = ClientDataFactory()
        
        cls.routine_length = 3
        cls.routines = RoutineFactory.create_batch(
            cls.routine_length,
            account=cls.auth_client.user
        )
        for routine in cls.routines:
            RoutineDayFactory(
                routine=routine,
                day="WED"
            )
            
        cls.url = reverse("routine-list")
        cls.success_msg = RoutineJSONRenderer.routine_msgs["list"]
    
    def setUp(self):
        self.auth_client.set_client_auth()
        
    def test_routine_list_success(self):
        """루틴 목록 조회 성공 테스트"""
        target_date = "2023-02-22"
        with freeze_time(target_date):
            self.auth_client.set_client_auth()
            RoutineResultFactory(
                result=RoutineResult.RESULT_CHOICES[1][0],
                routine=self.routines[1]
            )
            RoutineResultFactory(
                result=RoutineResult.RESULT_CHOICES[2][0],
                routine=self.routines[2]
            )
        
        self.auth_client.set_client_auth()
        res = self.auth_client.client.get(
            self.url,
            data={"today": target_date}
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["message"]["msg"], self.success_msg["msg"])
        self.assertEqual(res.data["message"]["status"], self.success_msg["status"])
        
        self.assertEqual(len(res.data["data"]), self.routine_length)
        for n in range(self.routine_length):
            self.assertEqual(res.data["data"][n]["goal"], self.routines[n].goal)
            self.assertEqual(res.data["data"][n]["title"], self.routines[n].title)
            self.assertEqual(res.data["data"][n]["result"], RoutineResult.RESULT_CHOICES[n][0])

    def test_routine_list_with_missing_param(self):
        """루틴 목록 조회 테스트(패러미터 누락)"""
        res = self.auth_client.client.get(
            self.url,
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_routine_list_with_missing_param(self):
        """루틴 목록 조회 테스트(패러미터 타입 불일치)"""
        res = self.auth_client.client.get(
            self.url,
            data={"today":"123"}
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        