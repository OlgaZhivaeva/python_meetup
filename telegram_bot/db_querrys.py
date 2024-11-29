from meetup.models import models


def check_participant(id):
    return Client.objects.filter(id_tg__exact=id).exists()


def get_participant(id):
    return Client.objects.get(id_tg__exact=id)


def create_participant(id, first_name, last_name, username=None, phone_number=None):
    Client.objects.create(
        id_tg=id,
        full_name=f"{first_name} {last_name} aka {username}",
        phone_number=phone_number,
    )
    return id