from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from adminsortable2.admin import SortableAdminBase
from adminsortable2.admin import SortableInlineAdminMixin

from .models import Meetup, Participant, Speech, Donation


class SpeechInline(SortableInlineAdminMixin, admin.TabularInline):
    model = Speech
    extra = 0


@admin.register(Speech)
class SpeechAdmin(admin.ModelAdmin):
    list_display = [
        'ordinal_number',
        'topic',
        'speaker',
        'time_limit',
        'meetup'
    ]
    ordering = ['meetup', 'ordinal_number']


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = [
        'tg_id',
        'full_name'
    ]


@admin.register(Meetup)
class MeetupAdmin(SortableAdminBase, admin.ModelAdmin):
    list_display = [
        'title',
        'date',
    ]
    inlines = [SpeechInline, ]


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = [
        'meetup',
        'donor',
        'amount'
    ]
