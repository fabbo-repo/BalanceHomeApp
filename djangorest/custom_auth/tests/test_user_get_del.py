from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from custom_auth.models import User, InvitationCode
import logging
import json
from django.conf import settings
import tempfile
from PIL import Image
import shutil
import os

class UserPutTests(APITestCase):
    def setUp(self):
        # Avoid WARNING logs while testing wrong requests 
        logging.disable(logging.WARNING)

        self.user_post_url=reverse('user_post')
        self.jwt_obtain_url=reverse('jwt_obtain_pair')
        self.change_password_url=reverse('change_password')

        # Create InvitationCode
        self.inv_code = InvitationCode.objects.create()
        self.inv_code.save()
        # User data
        self.user_data={
            "username":"username",
            "email":"email@test.com",
            "password": "password1@212",
            "password2": "password1@212",
            "inv_code": str(self.inv_code.code)
        }
        self.credentials = {
            "email": "email@test.com",
            "password": "password1@212"
        }
        # User creation
        user = User.objects.create(
            username=self.user_data["username"],
            email=self.user_data["email"],
            inv_code=self.inv_code,
            verified=True
        )
        user.set_password(self.user_data['password'])
        user.save()
        self.user_get_del_url=reverse('user_put_get_del', args=[user.id])
        # Jwt obtain
        self.jwt = self.jwt_obtain().data["access"]
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.jwt))
        return super().setUp()
    
    def jwt_obtain(self, credentials=None) :
        if credentials == None: credentials = self.credentials
        return self.client.post(
            self.jwt_obtain_url,
            data=json.dumps(credentials),
            content_type="application/json"
        )

    def user_get(self) :
        return self.client.get(
            self.user_get_del_url
        )
    
    def user_del(self) :
        return self.client.delete(
            self.user_get_del_url
        )

    """
    Checks that user data is correct
    """
    def test_get_user_data(self):
        response = self.user_get()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user_data2 = {
            "username": self.user_data["username"],
            "email": self.user_data["email"],
            "monthly_balance": 0,
            "annual_balance": 0,
        }
        self.assertEqual(response.data["username"], user_data2["username"])
        self.assertEqual(response.data["email"], user_data2["email"])
        self.assertEqual(response.data["monthly_balance"], user_data2["monthly_balance"])
        self.assertEqual(response.data["annual_balance"], user_data2["annual_balance"])

    """
    Checks that user gets deleted
    """
    def test_delete_user(self):
        response = self.user_del()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)