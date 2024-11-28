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
        verbose_name='время заполнения',
        auto_now_add=True,
    )
    stak = models.CharField(
        verbose_name='Стек',
        max_length=100,
    )
    communication = models.BooleanField(
        verbose_name='Общение',
        default=False,
    )

    class Meta:
        verbose_name = 'гость'
        verbose_name_plural = 'гости'

    def __str__(self):
        return self.name


class Speесн(models.Model):
    speaker = models.ForeignKey(
        Participant,
        verbose_name='Имя',
        on_delete=models.CASCADE,
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
        verbose_name = 'спикер'
        verbose_name_plural = 'спикеры'

    def __str__(self):
        return self.speaker.full_name


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

    class Meta:
        verbose_name = 'встреча'
        verbose_name_plural = 'встречи'

    def __str__(self):
        return self.name
