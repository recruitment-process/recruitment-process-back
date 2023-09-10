# Generated by Django 4.1 on 2023-09-07 15:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recruitment', '0003_alter_vacancy_job_conditions_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vacancy',
            name='deadline',
            field=models.DateField(default=datetime.date(2023, 10, 7), verbose_name='Срок закрытия вакансии'),
        ),
        migrations.AlterField(
            model_name='workexperience',
            name='end_date',
            field=models.DateField(blank=True, default=datetime.date(2023, 9, 7), null=True, verbose_name='Дата увольнения'),
        ),
    ]
