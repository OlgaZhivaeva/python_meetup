from meetup.models import Meetup, Participant, Questionnaire
from .extra_funcs import (
    get_datetime_now_with_inaccuracy_greater,
    get_datetime_now_with_inaccuracy_less,
)


def update_questionnaire(meetup, participant, full_name, stack, bio):
    Questionnaire.objects.update_or_create(
        participant=participant,
        meetup=meetup,
        defaults={
            'stack': stack,
            'bio': bio,
            'is_communicative': True
        }
    )
    participant.full_name = full_name
    participant.save()


# Получаем непросмотренную анкету
def get_unseen_questionnaire(participant_id, meetup_id, last_processed_id=None):
    if last_processed_id is None:
        questionnaire = Questionnaire.objects.filter(
            meetup__id=meetup_id
        ).exclude(participant__id=participant_id).order_by('id').first()
    else:
        questionnaire = Questionnaire.objects.filter(
            id__gt=last_processed_id, meetup__id=meetup_id
        ).exclude(participant__id=participant_id).order_by('id').first()
    return questionnaire


# Заполнил-ли юзер анкету
def check_questionnaire(participant, meetup_id):
    participant_id = participant.id
    return bool(
        Questionnaire.objects.filter(
            participant__id=participant_id,
            meetup__id=meetup_id
        ).first()
    )
    #return participant.questionnaires.filter(meetup__id__exact=meetup_id).first()


# Есть-ли хоть одна анкета
def check_questionnaires(participant_id, meetup_id):
    return bool(
        Questionnaire.objects.filter(
            meetup__id__exact=meetup_id
        ).exclude(participant__id__exact=participant_id).first()
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
    datetime_now_with_inaccuracy = get_datetime_now_with_inaccuracy_less()
    return Meetup.objects.filter(date__gt=datetime_now_with_inaccuracy)


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
