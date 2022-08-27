from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator

class BalanceUserManager(UserManager):

    def create_user(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        if not email:
            raise ValueError("The given email must be set")
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        if not email:
            raise ValueError("The given email must be set")
        return self._create_user(username, email, password, **extra_fields)


class User(AbstractUser):
    # Fields to iggnore in db form default User model:
    first_name = None
    last_name = None

    email = models.EmailField(
        _("email address"),
        unique=True,
    )
    # Expected annual balance at the end of a year, 
    # subtracted with the actual balance of each year
    annual_balance = models.FloatField(
        validators=[MinValueValidator(0.0)],
        default=0.0
    )
    # Expected monthly balance at the end of a month, 
    # subtracted with the actual balance of each month
    monthly_balance = models.FloatField(
        validators=[MinValueValidator(0.0)],
        default=0.0
    )
    # Field corresponding to email verification
    verified = models.BooleanField(
        default=False
    )
    # Date of the last code sent
    code_sent = models.DateTimeField(
        blank=True,
        null=True
    )

    objects = BalanceUserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [ "username" ]
    
    def __str__(self):
        return self.email