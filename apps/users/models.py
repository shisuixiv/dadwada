from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin,BaseUserManager


class UserManager(BaseUserManager):
        def create_user(self, phone, password=None, **extra_fields):
            """Создание обычного пользователя"""
            if not phone:
                raise ValueError("У пользователя должен быть номер телефона")
            user = self.model(phone=phone, **extra_fields)
            user.set_password(password)
            user.save(using=self._db)
            return user

        def create_superuser(self, phone, password=None, **extra_fields):
            """Создание суперпользователя"""
            extra_fields.setdefault("is_staff", True)
            extra_fields.setdefault("is_superuser", True)

            if extra_fields.get("is_staff") is not True:
                raise ValueError("Суперпользователь должен иметь is_staff=True.")
            if extra_fields.get("is_superuser") is not True:
                raise ValueError("Суперпользователь должен иметь is_superuser=True.")

            return self.create_user(phone, password, **extra_fields)

            

class User(AbstractBaseUser,PermissionsMixin):
        phone = models.CharField(max_length=20,unique=True, verbose_name="Номер телефона")
        name = models.CharField(max_length=155,verbose_name="Имя")

        is_active = models.BooleanField(default=True)
        is_staff = models.BooleanField(default=False)

        objects = UserManager()

        USERNAME_FIELD = 'phone'
        REQUIRED_FIELDS = []

        def __str__(self):
            return self.name
