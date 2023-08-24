# Generated by Django 4.1 on 2023-08-24 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_user_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='confirmation_code',
            field=models.CharField(default='99df278a-23ae-485c-8698-075cc78f76b8', editable=False, max_length=40),
        ),
        migrations.AddField(
            model_name='user',
            name='email_status',
            field=models.BooleanField(default=False, verbose_name='Подтверждена почта'),
        ),
    ]