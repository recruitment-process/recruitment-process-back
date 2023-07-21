from django.db import models
from multiselectfield import MultiSelectField


class Vacancy(models.Model):
    ''' Информация о вакансии '''
    EXPERIENCE = (
        ('1', 'Нет опыта'),
        ('2', '1-3 года'),
        ('3', '3-6 лет'),
        ('4', 'Более 6 лет'),
    )

    EMPLOYMENT_TYPE = (
        ('PO', 'Полная'),
        ('CH', 'Частичная'),
        ('PR', 'Проектная'),
        ('ST', 'Стажировка'),
        ('VO', 'Волонтерство'),
    )

    SCHEDULE_WORK = (
        ('P', 'Полный день'),
        ('S', 'Сменный график'),
        ('G', 'Гибкий график'),
        ('U', 'Удаленная работа'),
        ('W', 'Вахтовый метод'),
    )

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

    class Meta:
        ordering = ['company_title']
        verbose_name = 'Основная информация о компании'

    def __str__(self):
        return self.company_title



