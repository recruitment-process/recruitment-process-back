# Generated by Django 4.1 on 2023-08-29 15:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recruitment', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='vacancy',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vacancies', to=settings.AUTH_USER_MODEL, verbose_name='Автор'),
        ),
        migrations.AddField(
            model_name='vacancy',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vacancies', to='recruitment.company', verbose_name='Компания'),
        ),
        migrations.AddField(
            model_name='substage',
            name='stage',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='substage', to='recruitment.funnelstage', verbose_name='Этап воронки'),
        ),
        migrations.AddField(
            model_name='note',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_notes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='note',
            name='candidate',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recruitment.candidate', verbose_name='Кандидат'),
        ),
        migrations.AddField(
            model_name='funnelstage',
            name='candidate',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='funnel', to='recruitment.candidate', verbose_name='Кандидат'),
        ),
        migrations.AddField(
            model_name='event',
            name='candidate',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='candidate_events', to='recruitment.candidate'),
        ),
        migrations.AddField(
            model_name='education',
            name='resume',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='educations', to='recruitment.applicantresume', verbose_name='резюме'),
        ),
        migrations.AddField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='note',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notes', to='recruitment.note'),
        ),
        migrations.AddField(
            model_name='candidate',
            name='vacancy',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='candidates', to='recruitment.vacancy', verbose_name='Вакансия'),
        ),
        migrations.AddField(
            model_name='applicantresume',
            name='applicant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applicant_resumes', to=settings.AUTH_USER_MODEL, verbose_name='Соискатель'),
        ),
        migrations.AddField(
            model_name='applicantresume',
            name='work_experiences',
            field=models.ManyToManyField(blank=True, null=True, to='recruitment.workexperience', verbose_name='Информация об опыте работы'),
        ),
    ]