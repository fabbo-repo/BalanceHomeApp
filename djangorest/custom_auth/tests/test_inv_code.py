import uuid
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from custom_auth.models import User, InvitationCode
import logging

class InvitationCodeTests(APITestCase):
    def setUp(self):
        # Avoid WARNING logs while testing wrong requests 
        logging.disable(logging.WARNING)

        self.register_url=reverse('user_post')

        # Create InvitationCode
        self.inv_code = InvitationCode.objects.create()
        self.inv_code.save()
        # Test user data
        self.user_data={
            'username':"username",
            'email':"email@test.com",
            "password": "password1@212",
            "password2": "password1@212",
            'inv_code': self.inv_code.code
        }
        return super().setUp()

    """
    Checks that an invitation code gets updated after user registration
    """
    def test_inv_code_update(self):
        self.client.post(
            self.register_url,
            self.user_data
        )
        User.objects.get(email=self.user_data['email'])
        # Cheks if InvitationCode gets updated
        self.assertFalse(InvitationCode.objects.get(code=self.inv_code.code).is_active)
        
    """
    Checks that an user with inactive invitation code is not created
    """
    def test_user_with_inactive_inv_code(self):
        # Create inactive InvitationCode
        inv_code2 = InvitationCode.objects.create(
            is_active=False,
            usage_left=0
        )
        inv_code2.save()
        # Test user data 2
        user_data2={
            'username':"username",
            'email':"email@test.com",
            "password": "password1@212",
            "password2": "password1@212",
            'inv_code': inv_code2.code
        }
        
        response=self.client.post(
            self.register_url,
            user_data2
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('inv_code', response.data)
        
    """
    Checks that an user with no inv_code is not created
    """
    def test_wrong_inv_code(self):
        response=self.client.post(
            self.register_url,
            {
                'inv_cod': str(uuid.uuid4()),
                'username': self.user_data['username'],
                'email': self.user_data['email'],
                "password": self.user_data['password'],
                "password2": self.user_data['password2']
            }
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('inv_code', response.data)
   
    """
    Checks that an user with no inv_code is not created
    """
    def test_none_inv_code(self):
        response=self.client.post(
            self.register_url,
            {
                'username': self.user_data['username'],
                'email': self.user_data['email'],
                "password": self.user_data['password'],
                "password2": self.user_data['password2']
            }
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('inv_code', response.data)
   