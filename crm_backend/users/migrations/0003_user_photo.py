# Generated by Django 4.1 on 2023-07-19 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_remove_user_username_alter_user_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='users/', verbose_name='Фото'),
        ),
    ]
