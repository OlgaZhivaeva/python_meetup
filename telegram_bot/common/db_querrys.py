from meetup.models import Meetup, Participant, Speech

from .extra_funcs import (
    get_datetime_now_with_inaccuracy_greater,
    get_datetime_now_with_inaccuracy_less,
)


# Получаем доклад на митапе. Если у юзера есть доклад, то он спикер.
# Пока что не учитываем дубли.
def get_planning_speech(participant, meetup_id):
    return (
        Meetup.objects.get(id=meetup_id)
        .speeches.filter(speaker=participant)
        .first()
    )


def get_meetup(id):
    return Meetup.objects.prefetch_related("participants").get(id__exact=id)


def get_actual_meetups():
    datetime_now_with_inaccuracy_less = get_datetime_now_with_inaccuracy_less()
    datetime_now_with_inaccuracy_greater = (
        get_datetime_now_with_inaccuracy_greater()
    )
    return Meetup.objects.filter(
        date__gt=datetime_now_with_inaccuracy_less
    ).filter(date__lt=datetime_now_with_inaccuracy_greater)


def check_participant(id):
    return Participant.objects.filter(tg_id__exact=id).exists()


def get_participant(id):
    return Participant.objects.get(tg_id__exact=id)


def create_participant(id, first_name=None, last_name=None, username=None):
    return Participant.objects.create(
        tg_id=id, tg_username=username, full_name=f"{first_name} {last_name}"
    )


def add_participant_to_meetup(participant, meetup):
    meetup.participants.add(participant)
