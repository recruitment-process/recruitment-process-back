# Generated by Django 4.1 on 2023-09-10 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_remove_user_category_alter_user_confirmation_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='confirmation_code',
            field=models.CharField(default='283fa442-39c1-4839-887f-4be5d296d695', editable=False, max_length=40),
        ),
    ]
