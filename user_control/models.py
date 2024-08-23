import logging
from datetime import datetime

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken

from common.models import BaseModel

logger = logging.getLogger(__name__)


class MyUserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_verified', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


class UserModel(AbstractBaseUser, BaseModel, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    profile_picture = models.TextField(null=True, blank=True)
    otp = models.CharField(max_length=6, null=True, blank=True)
    otp_expiry = models.DateTimeField(null=True, blank=True)
    reset_password_token = models.CharField(
        max_length=255, null=True, blank=True,
        help_text='This token is used to reset the password',
    )
    reset_password_token_expiry = models.DateTimeField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        db_table = 'users'

        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.email

    def get_full_name(self):
        return str(self.first_name) + " " + str(self.last_name)

    def reset_password(self):
        self.set_password("111222")
        self.save()

    def update_last_login(self):
        """
        Updates the last login time for the user.
        """

        logger.info(f"Updating last login time for user: {self.email}")
        try:
            current_time = datetime.now()
            logger.info(f"Current time: {current_time}")
            self.last_login = current_time
            self.save()
        except Exception as e:
            logger.error(f"Error updating last login time: {e}")

    def update_profile_picture(self, profile_picture):
        """
        Updates the user's profile picture.

        :param profile_picture: Profile picture URL.
        """

        logger.info(f"Updating profile picture for user: {self.email}")
        try:
            self.profile_picture = profile_picture
            self.save()
            logger.info(f"Profile picture updated successfully.")
        except Exception as e:
            logger.error(f"Error updating profile picture: {e}")

    def tokens(self):
        tokens = RefreshToken.for_user(self)
        return {
            'refresh': str(tokens),
            'access': str(tokens.access_token),
        }

    def check_object_permissions(self, obj):
        if self.is_superuser:
            return True
        if self.is_staff:
            return True
        if self == obj.created_by:
            return True
        return False

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin
