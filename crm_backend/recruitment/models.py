from django.contrib.auth import get_user_model
from django.db import models
from multiselectfield import MultiSelectField
from django.core.validators import RegexValidator
from .utils import (EXPERIENCE, EMPLOYMENT_TYPE, SCHEDULE_WORK)

User = get_user_model()


class Company(models.Model):
    ''' Информация о компании '''
    company_title = models.CharField(
        max_length=100,
        verbose_name='Название компании',
    )
    about_company = models.TextField(
        verbose_name = 'О компании',
        help_text='Введите информацию о компани'
    )

    company_address = models.CharField(
        max_length=100,
        verbose_name='Адрес компании',
    )

    email = models.EmailField(verbose_name='Эл.почта',)

    phoneNumberRegex = RegexValidator(regex=r"^\+?1?\d{8,15}$")

    phoneNumber = models.CharField(
        validators=[phoneNumberRegex],
        max_length=16,
    )

    link_hr = models.URLField(max_length=100, verbose_name = 'Ссылка на HR',)


    class Meta:
        ordering = ['company_title']
        verbose_name = 'Основная информация о компании'

    def __str__(self):
        return self.company_title


class Vacancy(models.Model):
    ''' Информация о вакансии '''

    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, verbose_name='Компания', related_name='vacancys')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='Автор', related_name='vacancys')

    vacancy_title = models.CharField(
        max_length=100,
        verbose_name='Название вакансии',
    )

    required_experience = models.CharField(
        max_length=1,
        choices=EXPERIENCE,
        verbose_name='Требуемый опыт работы',
        blank=False,
    )
    
    employment_type = MultiSelectField(
        max_length=3,
        choices=EMPLOYMENT_TYPE,
        verbose_name='Тип занятости',
        blank=False,
    )

    schedule_work = MultiSelectField(
        max_length=3,
        choices=SCHEDULE_WORK,
        verbose_name='Расписание работы',
        blank=False,
    )

    about_company = models.TextField(
        verbose_name = 'О компании',
        help_text='Введите информацию о компани'
    )

    pub_date = models.DateTimeField(
        'Дата публикации вакансии',
        auto_now_add=True)
    
    job_conditions = models.TextField(
        verbose_name = 'Условия работы',
        help_text='Введите условия работы'
    )

    job_responsibilities = models.TextField(
        verbose_name = 'Обязанности кондидата',
        help_text='Введите обязанности кондидата'
    )

    technology_stack = models.TextField( # позже можно будет сделать бд со всеми навыками 
        verbose_name = 'Ключевые навыки',
    )

    class Meta:
        ordering = ['pub_date']
        verbose_name = 'Основная информация о вакансии'

    def __str__(self):
        return self.vacancy_title
