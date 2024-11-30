from meetup.models import Participant, Meetup, Speech
from .extra_funcs import (
    get_datetime_now_with_inaccuracy_less
)


# Получаем доклад на митапе. Если у юзера есть доклад, то он спикер.
# Пока что не учитываем дубли.
def get_planning_speech(user_id, meetup_id):
    speech = Meetup.objects.get(
        id=meetup_id
    ).speeches.filter(speaker__tg_id=user_id)
    if speech.exists():
        return speech.first()
    else:
        return None


def get_meetup(id):
    return Meetup.objects.get(id__exact=id)


def get_actual_meetups():
    datetime_now_with_inaccuracy = get_datetime_now_with_inaccuracy_less()
    return Meetup.objects.filter(date__gt=datetime_now_with_inaccuracy)


def check_participant(id):
    return Participant.objects.filter(tg_id__exact=id).exists()


def get_participant(id):
    return Participant.objects.get(tg_id__exact=id)


def create_participant(id, first_name=None, last_name=None, username=None):
    Participant.objects.create(
        tg_id=id,
        tg_username=username,
        full_name=f"{first_name} {last_name}"
    )
    return id
