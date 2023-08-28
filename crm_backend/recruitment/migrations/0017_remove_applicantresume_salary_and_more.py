# Generated by Django 4.1 on 2023-08-25 06:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recruitment', '0016_rename_status_vacancy_vacancy_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='applicantresume',
            name='salary',
        ),
        migrations.AlterField(
            model_name='vacancy',
            name='vacancy_status',
            field=models.CharField(choices=[('A', 'activeVacancies'), ('F', 'completedVacancies'), ('D', 'draftVacancies')], default='D', max_length=1, verbose_name='Статус вакансии'),
        ),
    ]