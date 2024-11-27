from django.contrib import admin

from .models import Meetup, Speaker,Guest

@admin.register(Speaker)
class SpeakerAdmin(admin.ModelAdmin):
    search_fields = [
        'number',
        'tg_id',
        'name',
        'topic',
    ]
    list_display = [
        'number',
        'tg_id',
        'name',
        'topic',
    ]
    ordering = ['number']


@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    search_fields = [
        'tg_id',
        'name',
        'filled_in',
    ]
    list_display = [
        'tg_id',
        'name',
        'filled_in',
    ]

@admin.register(Meetup)
class MeetupAdmin(admin.ModelAdmin):
    search_fields = [
        'beginning',
        'time_limit',
        'address',
    ]
    list_display = [
        'beginning',
        'time_limit',
        'address',
    ]