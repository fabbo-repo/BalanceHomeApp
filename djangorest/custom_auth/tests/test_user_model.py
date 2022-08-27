from rest_framework.test import APITestCase
from custom_auth.models import User

class TestModel(APITestCase):
    def setUp(self):
        self.user_data={
            'username':"username",
            'email':"email@test.com",
            "password": "password1@212"
        }
        return super().setUp()
    
    def register_user(self):
        return User.objects.create_user(**self.user_data)

    def register_super_user(self):
        return User.objects.create_superuser(**self.user_data)

    """
    Checks if User is created  as norma user
    """
    def test_creates_user(self):
        user = self.register_user()
        self.assertEqual(user.username, "username")
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    """
    Checks if User is created as super user
    """
    def test_creates_super_user(self):
        user = self.register_super_user()
        self.assertEqual(user.username, "username")
        self.assertEqual(user.is_staff, True)
        self.assertEqual(user.is_superuser, True)

    """
    Checks that an User with is_staff set to False
    raises an Exception when it is created as super user
    """
    def test_creates_super_user_with_is_staff(self):
        self.assertRaises(
            ValueError, 
            User.objects.create_superuser,
            is_staff=False,
            **self.user_data
        )
        with self.assertRaisesMessage(ValueError, 'Superuser must have is_staff=True.'):
            User.objects.create_superuser(
                is_staff=False,
                **self.user_data
            )

    """
    Checks that an User with is_superuser set to False
    raises an Exception when it is created as super user
    """
    def test_creates_super_user_with_is_superuser(self):
        self.assertRaises(
            ValueError, 
            User.objects.create_superuser,
            is_superuser=False,
            **self.user_data
        )
        with self.assertRaisesMessage(
            ValueError, 
            'Superuser must have is_superuser=True.'):
            User.objects.create_superuser(
                is_superuser=False,
                **self.user_data
            )
    
    """
    Checks that an User without username (same as empty or None)
    raises an Exception when it is created
    """
    def test_cant_create_user_without_username(self):
        self.assertRaises(
            ValueError, 
            User.objects.create_user, 
            email=self.user_data['email'],
            password=self.user_data['password'],
            username=""
        )
        with self.assertRaisesMessage(ValueError, 'The given username must be set'):
            User.objects.create_user(
                email=self.user_data['email'],
                password=self.user_data['password'],
                username=""
            )

    """
    Checks that an User without email (same as empty or None)
    raises an Exception when it is created
    """
    def test_cant_create_user_without_email(self):
        self.assertRaises(
            ValueError, 
            User.objects.create_user,
            email='',
            password=self.user_data['password'],
            username=self.user_data['username']
        )
        with self.assertRaisesMessage(ValueError, 'The given email must be set'):
            User.objects.create_user(
                email='',
                password=self.user_data['password'],
                username=self.user_data['username']
            )