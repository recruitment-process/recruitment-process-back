# Generated by Django 4.1 on 2023-09-09 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_user_phone_number_user_position_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='category',
        ),
        migrations.AlterField(
            model_name='user',
            name='confirmation_code',
            field=models.CharField(default='7b50c2a5-fb6d-44e8-8321-3419e317c980', editable=False, max_length=40),
        ),
    ]