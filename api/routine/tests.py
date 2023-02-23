from copy import deepcopy

from freezegun import freeze_time
from rest_framework import status
from rest_framework.test import APIClient

from api.auth.tests import AuthTestCore

class RoutineTestCore:
    def do_create_routine(self, data):
        res = self.client.post(
            "/api/routine/",
            data=data
        )
        return res
    
    def do_update_routine(self, routine_id, data):
        res = self.client.patch(
            f"/api/routine/{routine_id}/",
            data=data
        )
        return res
    
    def do_delete_routine(self, routine_id):
        res = self.client.delete(
            f"/api/routine/{routine_id}/"            
        )
        return res
        
    def do_get_retrieve_routine(self, routine_id):
        res = self.client.get(
            f"/api/routine/{routine_id}/"
        )
        return res
    
    def do_get_list_routine(self, data):
        res = self.client.get(
            "/api/routine/",
            data=data,
        )
        return res
    
    def do_update_result_routine(self,routine_id, data):
        res = self.client.post(
            f"/api/routine/{routine_id}/result/",
            data=data
        )
        return res


class RoutineTestCase(RoutineTestCore, AuthTestCore):
    client = APIClient()
    
    def _auth_setUp(self):
        self.email = "routine@test.com"
        self.password = "1routine!"
        self.username = "routine_tester"
        
        data = {
            "email": self.email,
            "password": self.password,
            "username": self.username
        }
        
        super().do_register(data)
        
    def _example_data_setUp(self):
        self.create_data = {
            "title" : "problem solving",
            "category" : "HOMEWORK",
            "goal": "Increase your problem-solving skills",
            "is_alarm": True,
            "days": ["MON", "WED", "FRI"]
        }
    
    def setUp(self):
        self._auth_setUp()
        self._example_data_setUp()
        self.do_set_credential()
        
    def do_set_credential(self):
        data = {
            "email": self.email,
            "password": self.password
        }
        res = super().do_login(data)
        token = res.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        
    def do_get_new_routine(self):
        res = super().do_create_routine(self.create_data)
        
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data["message"]["status"], "ROUTINE_CREATE_OK")
        
        return res.data["data"]["routine_id"]
        
    def test_create_routine_success(self):
        self.do_get_new_routine()
        
    def test_create_routine_error(self):
        # choicefield missing
        data = deepcopy(self.create_data)
        data["category"] = "TEST"
        res = super().do_create_routine(data)
        
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        
        # multiple choicefield missing
        data["category"] = "HOMEWORK"
        data["days"][0] = "TEST_VALUE"
        res = super().do_create_routine(data)
        
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        
        # require field missing
        data["days"][0] = "MON"
        data.pop("goal")
        res = super().do_create_routine(data)  
        
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_update_routine_success(self):
        routine_id = self.do_get_new_routine()
        update_data = {
            "title": "Edited problem solving",
            "days": ["TUE", "SAT"]
        }
        res = super().do_update_routine(routine_id, update_data)
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["message"]["status"], "ROUTINE_UPDATE_OK")
        
    def test_update_routine_error(self):
        routine_id = self.do_get_new_routine()
        
        # update invalid routine
        update_data = {
            "title": "Edited problem solving",
            "days": ["TUE", "SAT"]
        }
        res = super().do_update_routine(1234567, update_data)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        
        # update to invalid category
        update_data = {
            "category": "None"
        }
        res = super().do_update_routine(routine_id, update_data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        
        # update to invalid days
        update_data = {
            "days": ["TUE", "None"]
        }
        res = super().do_update_routine(routine_id, update_data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_delete_routine_success(self):
        routine_id = self.do_get_new_routine()
        res = super().do_delete_routine(routine_id)
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["message"]["status"], "ROUTINE_DELETE_OK")
        
    def test_delete_routine_error(self):
        # delete invalid routine
        res = super().do_delete_routine(1234567)
        
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_get_retrieve_routine_success(self):
        routine_id = self.do_get_new_routine()
        res = super().do_get_retrieve_routine(routine_id)
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["message"]["status"], "ROUTINE_DETAIL_OK")
        
    def test_get_retrieve_routine_error(self):
        # get invalid routine
        res = super().do_get_retrieve_routine(1234567)
        
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        
    def test_get_list_routine_success(self):
        # create routine on sunday
        # routine days = MON, WED, FRI
        with freeze_time("2023-02-19"):
            self.do_set_credential()
            self.do_get_new_routine()
        
        # get list monday's data on wednesday
        with freeze_time("2023-02-22"):
            self.do_set_credential()
            data = {"today": "2023-02-20"}
            res = super().do_get_list_routine(data)
            
            self.assertEqual(res.status_code, status.HTTP_200_OK)
            self.assertEqual(res.data["message"]["status"], "ROUTINE_LIST_OK")
            
    def test_get_list_routine_error(self):
        # date param missing
        data = {}  
        res = super().do_get_list_routine(data)
        
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        
        # invalid today date format
        data = {"today": "2023-02"}
        res = super().do_get_list_routine(data)
        
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_update_result_routine_success(self):
        routine_id = None
        with freeze_time("2023-02-19"):
            self.do_set_credential()
            routine_id = self.do_get_new_routine()
            
        with freeze_time("2023-02-23"):
            self.do_set_credential()
            data = {
                "today": "2023-02-22",
                "result": "DONE"
            }
            res = super().do_update_result_routine(routine_id, data)
            
            self.assertEqual(res.status_code, status.HTTP_200_OK)
            self.assertEqual(res.data["message"]["status"], "ROUTINE_RESULT_UPDATE_OK")
        
        with freeze_time("2023-02-23"):
            self.do_set_credential()
            res = super().do_get_retrieve_routine(routine_id)
            
            self.assertEqual(res.data["data"]["result"], "DONE")
            
    def test_update_result_routine_error(self):
        routine_id = None
        with freeze_time("2023-02-19"):
            self.do_set_credential()
            routine_id = self.do_get_new_routine()
        
        self.do_set_credential()
        
        # today not contain routine days
        data = {
            "today": "2023-02-21",
            "result": "DONE"
        }
        res = super().do_update_result_routine(routine_id, data)
        
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        
        # invalid result value
        data = {
            "today": "2023-02-21",
            "result": "NO DATA"
        }
        res = super().do_update_result_routine(routine_id, data)
        
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        
        # missing required field
        data = {
            "result": "NO DATA"
        }
        res = super().do_update_result_routine(routine_id, data)
        
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_create_update_delete_routine(self):
        """
        시나리오: 2023년
        1. 2월 20일(월)에
            1. 루틴 A 생성
            2. 2월 20일의 루틴 A 결과를 DONE으로 수정
        2. 2월 22일(수)에
            1. 2월 20일 루틴 목록 출력
            2. 루틴 A 단건 출력
            3. 루틴 A 삭제
        """
        routine_A = None
        
        with freeze_time("2022-02-20"):
            self.do_set_credential()
            routine_A = self.do_get_new_routine()
            
            data = {
                "today": "2023-02-20",
                "result": "DONE"
            }
            res = super().do_update_result_routine(routine_A, data)
            self.assertEqual(res.status_code, status.HTTP_200_OK)
            
        with freeze_time("2022-02-20"):
            self.do_set_credential()
            
            data = {"today": "2023-02-20"}
            res = super().do_get_list_routine(data)
            self.assertEqual(res.status_code, status.HTTP_200_OK)
            self.assertEqual(len(res.data["data"]), 1)
            self.assertEqual(res.data["data"][0]["result"], "DONE")
            
            res = super().do_get_retrieve_routine(routine_A)
            self.assertEqual(res.status_code, status.HTTP_200_OK)
            self.assertEqual(res.data["data"]["result"], "NOT")
            
            res = super().do_delete_routine(routine_A)
            self.assertEqual(res.status_code, status.HTTP_200_OK)
