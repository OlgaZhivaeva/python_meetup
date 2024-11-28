from django.db import models
from django.core.validators import MinValueValidator


class Participant(models.Model):
    tg_id = models.IntegerField(
        verbose_name='Телеграмм ID',
        unique=True,
        db_index=True,
    )
    tg_username = models.CharField(
        verbose_name='Никнейм',
        unique=True,
        max_length=50,
        blank=True,
        null=True,
        db_index=True,
    )
    bio = models.TextField(
        verbose_name='О себе',
        blank=True,
        null=True
    )
    stack = models.CharField(
        verbose_name='Стек',
        max_length=200,
        blank=True,
        null=True
    )
    full_name = models.CharField(
        verbose_name='Полное имя',
        max_length=100,
        db_index=True,
    )
    filled_at = models.DateTimeField(
        verbose_name='Время заполнения',
        auto_now_add=True,
    )
    is_communicative = models.BooleanField(
        verbose_name='Готов к общению',
        default=False,
    )

    class Meta:
        verbose_name = 'Участник'
        verbose_name_plural = 'Участники'

    def __str__(self):
        return self.full_name


class Meetup(models.Model):
    title = models.CharField(
        verbose_name='Название',
        max_length=200,
        db_index=True,
    )
    date = models.DateTimeField(
        verbose_name='Дата конференции',
        db_index=True,
    )
    address = models.CharField(
        verbose_name='Адрес',
        max_length=200,
        null=True,
        blank=True,
    )
    participants = models.ManyToManyField(
        Participant,
        verbose_name='Участники',
        related_name='meetups'
    )

    class Meta:
        verbose_name = 'Встреча'
        verbose_name_plural = 'Встречи'

    def __str__(self):
        return f'{self.title} {self.date}'


class Donation(models.Model):
    meetup = models.ForeignKey(
        Meetup,
        on_delete=models.CASCADE,
        db_index=True,
        verbose_name='Конференция'
    )
    donor = models.ForeignKey(
        Participant,
        on_delete=models.SET_NULL,
        null=True,
        db_index=True,
        verbose_name='Донатор'
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Сумма'
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Время доната'
    )

    class Meta:
        verbose_name = 'Пожертвование'
        verbose_name_plural = 'Пожертвования'

    def __str__(self):
        return f"Донат от {self.donor} на {self.meetup.title}"


class Speech(models.Model):
    speaker = models.ForeignKey(
        Participant,
        verbose_name='Имя',
        on_delete=models.SET_NULL,
        null=True,
        db_index=True
    )
    topic = models.CharField(
        verbose_name='Тема выступления',
        max_length=200,
        db_index=True,
    )
    ordinal_number = models.PositiveIntegerField(
        verbose_name='№ п/п',
        null=True,
        blank=True,
    )
    time_limit = models.PositiveIntegerField(
        verbose_name='Время выступления',
        validators=[MinValueValidator(10)],
    )
    meetup = models.ForeignKey(
        Meetup,
        related_name='speeches',
        verbose_name='Конференция',
        on_delete=models.CASCADE,
        db_index=True
    )

    class Meta:
        verbose_name = 'Доклад'
        verbose_name_plural = 'Доклады'
        ordering = ['ordinal_number']

    def __str__(self):
        return f'{self.topic} {self.speaker.full_name}'
