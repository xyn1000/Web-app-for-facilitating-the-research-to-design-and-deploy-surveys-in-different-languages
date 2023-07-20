# Create your tests here.
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.test import APITestCase
import jmespath


class ClinicTestCase(APITestCase):

    #successful survey request
    def test_survey1(self):
        client = APIClient()
        resp = client.get("/account/response/5/")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        
    #unsuccessful survey request - survey doesn't exist
    def test_survey2(self):
        client = APIClient()
        resp = client.get("/account/response/1/")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)