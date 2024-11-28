from django.contrib import admin

from .models import Meetup, Participant, Speech

@admin.register(Speech)
class SpeechAdmin(admin.ModelAdmin):
    search_fields = [
        'ordinal',
        'speaker'
        'topic',
        'time_limit',
    ]
    list_display = [
        'ordinal',
        'speaker',
        'topic',
        'time_limit',
    ]
    ordering = ['ordinal']


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    search_fields = [
        'tg_id',
        'user_name',
        'full_name',
        'filled_at',
        'stack',
        'communication',
    ]
    list_display = [
        'tg_id',
        'user_name',
        'full_name',
        'filled_at',
        'stack',
        'communication',
    ]

@admin.register(Meetup)
class MeetupAdmin(admin.ModelAdmin):
    search_fields = [
        'name',
        'beginning',
        'address',
    ]
    list_display = [
        'name',
        'beginning',
        'address',
    ]