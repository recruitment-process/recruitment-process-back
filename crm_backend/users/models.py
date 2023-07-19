from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class Role(models.TextChoices):
    ''' Два типа пользователей сервиса: Соискатели и HR. '''
    APPLICANT = 'Соискатель'
    HR = 'HR'


class Category(models.Model):
    ''' Категория соискателя: разработка, бухгалтерия, обслуживание и т.д. '''
    name = models.CharField(max_length=100, verbose_name='Название')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['id']

    def __str__(self):
        return self.name


class UserManager(BaseUserManager):
    ''' Кастомный менеджер для кастомной модели пользователя. '''
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
    ''' Кастомная модель пользователя. '''
    username = None
    USERNAME_FIELD = 'email'
    email = models.EmailField(max_length=254, unique=True)
    first_name = models.CharField(max_length=150, verbose_name='Имя')
    last_name = models.CharField(max_length=150, verbose_name='Фамилия')
    role = models.CharField(
        max_length=11,
        choices=Role.choices,
        default=Role.APPLICANT,
        verbose_name='Роль'
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        verbose_name='Категория', null=True
    )
    photo = models.ImageField(
        upload_to='users/', null=True, blank=True, verbose_name='Фото')
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
