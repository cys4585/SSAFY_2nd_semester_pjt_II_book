from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, AbstractBaseUser
# Create your models here.


class User(AbstractUser):
    # nickname = models.CharField(max_length=20, null=True)
    # kakao_uid = models.BigIntegerField(null=True)
    pass

    # class UserManager(BaseUserManager):
    #     def create_user(self, user_mail, username, password=None):
    #         if not user_mail:
    #             raise ValueError("Users must have an user_mail address")

    #         user = self.model(user_mail=user_mail, username=username)

    #         user.set_password(password)
    #         user.save(using=self._db)
    #         return user

    #     def create_superuser(self, user_mail, username='admin', password=None):
    #         user = self.create_user(
    #             user_mail, password=password, username=username)
    #         user.is_admin = True
    #         user.save(using=self._db)
    #         return user

    # class User(AbstractBaseUser):
    #     username = models.CharField(max_length=20)
    #     user_mail = models.EmailField(unique=True)
    #     user_img = models.CharField(max_length=200, null=True)
    #     gender = models.CharField(max_length=10, null=True)
    #     age_range = models.CharField(max_length=10, null=True)
    #     user_birthdate = models.DateField(null=True)

    #     password = models.CharField(max_length=255, null=True)
    #     is_admin = models.BooleanField(default=False)
    #     is_active = models.BooleanField(default=True)
    #     created_on = models.DateTimeField(auto_now_add=True)
    #     updated_on = models.DateTimeField(auto_now=True)

    #     objects = UserManager()

    #     USERNAME_FIELD = 'user_mail'
    #     REQUIRED_FIELDS = []

    #     def has_perm(self, perm, obj=None):
    #         "Does the user have a specific permission?"
    #         # Simplest possible answer: Yes, always
    #         return True

    #     def has_module_perms(self, app_label):
    #         "Does the user have permissions to view the app `app_label`?"
    #         # Simplest possible answer: Yes, always
    #         return True

    #     @property
    #     def is_staff(self):
    #         "Is the user a member of staff?"
    #         # Simplest possible answer: All admins are staff
    #         return self.is_admin
