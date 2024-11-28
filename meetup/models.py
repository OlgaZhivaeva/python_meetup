from django.db import models
from django.core.validators import MinValueValidator


class Participant(models.Model):
    tg_id = models.CharField(
        verbose_name='Телеграмм ID',
        max_length=50,
        unique=True,
    )
    user_name = models.CharField(
        verbose_name='Ник',
        max_length=50,
        unique=True,
    )
    full_name = models.CharField(
        verbose_name='Имя',
        max_length=100,
    )
    filled_at = models.DateTimeField(
        verbose_name='Время заполнения',
        auto_now_add=True,
    )
    stack = models.CharField(
        verbose_name='Стек',
        max_length=100,
    )
    communication = models.BooleanField(
        verbose_name='Общение',
        default=False,
    )

    class Meta:
        verbose_name = 'Участник'
        verbose_name_plural = 'Участники'

    def __str__(self):
        return self.full_name


class Speech(models.Model):
    speaker = models.ForeignKey(
        Participant,
        verbose_name='Спикер',
        on_delete=models.SET_NULL,
        null=True,
    )
    topic = models.CharField(
        verbose_name='Тема выступления',
        max_length=200,
    )
    ordinal = models.PositiveIntegerField(
        unique=True,
        null=True,
        blank=True,
    )
    time_limit = models.PositiveIntegerField(
        verbose_name='Время выступления',
        unique=True,
        validators=[MinValueValidator(10)],
    )

    class Meta:
        verbose_name = 'Доклад'
        verbose_name_plural = 'Доклады'

    def __str__(self):
        return self.topic


class Meetup(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=200,
        blank=True,
    )
    beginning = models.DateTimeField(
        verbose_name='Начало',
    )
    address = models.CharField(
        verbose_name='Адрес',
        max_length=200,
        null=True,
        blank=True,
    )
    speeches = models.ManyToManyField(
        Speech,
        verbose_name='Доклады',
        related_name='meetups',
    )
    participant = models.ManyToManyField(
        Participant,
        verbose_name='Участники',
        related_name='meetups',
    )

    class Meta:
        verbose_name = 'Встреча'
        verbose_name_plural = 'Встречи'

    def __str__(self):
        return self.name
