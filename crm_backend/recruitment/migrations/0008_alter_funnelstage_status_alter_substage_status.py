# Generated by Django 4.1 on 2023-08-22 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recruitment', '0007_funnelstage_substage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='funnelstage',
            name='status',
            field=models.CharField(choices=[('1', 'Создан'), ('2', 'Пройден'), ('3', 'Провален')], default='1', max_length=5, verbose_name='Статус этапа'),
        ),
        migrations.AlterField(
            model_name='substage',
            name='status',
            field=models.CharField(choices=[('1', 'Создан'), ('2', 'Пройден'), ('3', 'Провален')], default='1', max_length=5, verbose_name='Статус подэтапа'),
        ),
    ]