# Generated by Django 4.1 on 2023-09-03 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recruitment', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vacancy',
            name='job_conditions',
            field=models.TextField(blank=True, help_text='Введите условия работы', max_length=1400, null=True, verbose_name='Условия работы'),
        ),
        migrations.AlterField(
            model_name='vacancy',
            name='job_responsibilities',
            field=models.TextField(blank=True, help_text='Введите обязанности кандидата', max_length=1400, null=True, verbose_name='Обязанности кандидата'),
        ),
    ]
