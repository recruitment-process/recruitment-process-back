# Generated by Django 4.1 on 2023-08-24 13:49

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('recruitment', '0010_merge_20230824_2044'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='applicantresume',
            name='marital_status',
        ),
        migrations.AddField(
            model_name='applicantresume',
            name='pub_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Дата публикации резюме'),
            preserve_default=False,
        ),
    ]
