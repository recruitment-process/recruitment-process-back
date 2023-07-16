from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class Role(models.TextChoices):
    APPLICANT = 'Соискатель'
    HR = 'HR'


class Category(models.TextChoices):
    DEVELOPER = 'Разработчик'
    HR = 'Кадровик'
    ACCOUNTANT = 'Бухгалтер'
    SERVICE = 'Обслуживающий персонал'
    MANAGMENT = 'Управление'


class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    USERNAME_FIELD = 'email'
    email = models.EmailField(max_length=254, unique=True)
    first_name = models.CharField(max_length=150, verbose_name='Имя')
    last_name = models.CharField(max_length=150, verbose_name='Фамилия')
    role = models.CharField(
        max_length=11,
        choices=Role.choices,
        default=Role.APPLICANT
    )
    category = models.CharField(
        max_length=50,
        choices=Category.choices,
        default=Category.SERVICE
    )
    REQUIRED_FIELDS = []
    objects = UserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['id']

    @property
    def is_applicant(self):
        return self.role == Role.APPLICANT

    @property
    def is_hr(self):
        return self.role == Role.HR

    def __str__(self):
        return self.email
