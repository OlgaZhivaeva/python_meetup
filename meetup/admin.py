from datetime import timedelta
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from adminsortable2.admin import SortableAdminBase
from adminsortable2.admin import SortableInlineAdminMixin

from .models import Meetup, Participant, Speech, Donation


class SpeechInline(SortableInlineAdminMixin, admin.TabularInline):
    model = Speech
    fields = [
        'ordinal_number',
        'get_time',
        'time_limit',
        'topic',
        'speaker',
    ]
    readonly_fields = ['get_time',]
    extra = 0

    def get_time(self, obj):
        date = obj.meetup.date
        for num in range(1, obj.ordinal_number):
            minutes = Speech.objects.get(meetup=obj.meetup, ordinal_number=num).time_limit
            date += timedelta(minutes=minutes)
        date += timedelta(minutes=180)
        return date.time().strftime("%H:%M")


@admin.register(Speech)
class SpeechAdmin(admin.ModelAdmin):
    list_display = [
        'ordinal_number',
        'get_time',
        'time_limit',
        'topic',
        'speaker',
        'meetup',
    ]
    list_filter = ['meetup',]
    ordering = ['meetup', 'ordinal_number']

    def get_time(self, obj):

        date = obj.meetup.date
        for num in range(1, obj.ordinal_number):
            minutes = Speech.objects.get(meetup=obj.meetup, ordinal_number=num).time_limit
            date += timedelta(minutes=minutes)
        date += timedelta(minutes=180)
        return date.time().strftime("%H:%M")


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = [
        'tg_id',
        'tg_username',
        'bio',
        'stack',
        'full_name',
        'is_communicative',
    ]
    list_filter = ['meetups',]


@admin.register(Meetup)
class MeetupAdmin(SortableAdminBase, admin.ModelAdmin):
    list_display = [
        'title',
        'date',
        'address',
    ]
    inlines = [SpeechInline, ]


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = [
        'meetup',
        'donor',
        'amount'
    ]
