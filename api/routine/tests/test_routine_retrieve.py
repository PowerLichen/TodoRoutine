from freezegun import freeze_time
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from api.routine.renderers import RoutineJSONRenderer
from lib.factory.client_factory import ClientDataFactory
from lib.factory.routine_factory import RoutineFactory
from lib.factory.routine_factory import RoutineDayFactory
from lib.factory.routine_factory import RoutineResultFactory


class RoutineRetrieveTestCase(APITestCase):
    @classmethod
    @freeze_time("2023-02-20")
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
        cls.success_msg = RoutineJSONRenderer.routine_msgs["retrieve"]
        
    def setUp(self):
        self.auth_client.set_client_auth()
        
    def test_routine_retrieve_success(self):
        """루틴 단건 조회 성공 테스트"""
        res = self.auth_client.client.get(
            self.url
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["message"]["msg"], self.success_msg["msg"])
        self.assertEqual(res.data["message"]["status"], self.success_msg["status"])
        self.assertEqual(res.data["data"]["result"], "NOT")
        
    def test_routine_retrieve_with_invalid_pk(self):
        """루틴 단건 조회 테스트 (유효하지 않은 pk)"""
        res = self.auth_client.client.get(
            reverse("routine-detail", kwargs={"pk": 100})
        )
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        
    def test_routine_retrieve_compare_result_in_difference_date(self):
        """루틴 단건 조회 테스트 (기록된 result 값을 서로 다른 날짜로 조회)"""
        RoutineDayFactory(routine=self.routine, day="WED")
        
        with freeze_time("2023-02-22"):
            self.auth_client.set_client_auth()
            RoutineResultFactory(
                result="TRY",
                routine=self.routine
            )
            
            res = self.auth_client.client.get(
                self.url
            )
            self.assertEqual(res.status_code, status.HTTP_200_OK)
            self.assertEqual(res.data["data"]["result"], "TRY")
        
        self.auth_client.set_client_auth()
        res = self.auth_client.client.get(
            self.url
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["data"]["result"], "NOT")
