# Generated by Django 5.1 on 2024-12-01 19:16

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tg_id', models.IntegerField(db_index=True, unique=True, verbose_name='Телеграмм ID')),
                ('tg_username', models.CharField(blank=True, db_index=True, max_length=50, null=True, unique=True, verbose_name='Никнейм')),
                ('full_name', models.CharField(blank=True, db_index=True, max_length=100, null=True, verbose_name='Полное имя')),
            ],
            options={
                'verbose_name': 'Участник',
                'verbose_name_plural': 'Участники',
            },
        ),
        migrations.CreateModel(
            name='Meetup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=200, verbose_name='Название')),
                ('date', models.DateTimeField(db_index=True, verbose_name='Дата конференции')),
                ('address', models.CharField(blank=True, max_length=200, null=True, verbose_name='Адрес')),
                ('participants', models.ManyToManyField(related_name='meetups', to='meetup.participant', verbose_name='Участники')),
            ],
            options={
                'verbose_name': 'Встреча',
                'verbose_name_plural': 'Встречи',
            },
        ),
        migrations.CreateModel(
            name='Donation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Сумма')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Время доната')),
                ('meetup', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='donations', to='meetup.meetup', verbose_name='Конференция')),
                ('donor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='donations', to='meetup.participant', verbose_name='Донатор')),
            ],
            options={
                'verbose_name': 'Пожертвование',
                'verbose_name_plural': 'Пожертвования',
            },
        ),
        migrations.CreateModel(
            name='Questionnaire',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField(blank=True, null=True, verbose_name='О себе')),
                ('stack', models.CharField(blank=True, max_length=200, null=True, verbose_name='Стек')),
                ('meetup', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questionnaires', to='meetup.meetup', verbose_name='Конференция')),
                ('participant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questionnaires', to='meetup.participant', verbose_name='Участник')),
            ],
            options={
                'verbose_name': 'Анкета',
                'verbose_name_plural': 'Анкеты',
            },
        ),
        migrations.CreateModel(
            name='Speech',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic', models.CharField(db_index=True, max_length=200, verbose_name='Тема выступления')),
                ('ordinal_number', models.PositiveIntegerField(blank=True, null=True, verbose_name='№ п/п')),
                ('time_limit', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(10)], verbose_name='Время выступления')),
                ('meetup', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='speeches', to='meetup.meetup', verbose_name='Конференция')),
                ('speaker', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='speeches', to='meetup.participant', verbose_name='Имя')),
            ],
            options={
                'verbose_name': 'Доклад',
                'verbose_name_plural': 'Доклады',
                'ordering': ['ordinal_number'],
            },
        ),
    ]
