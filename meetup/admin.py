from datetime import timedelta
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import path

from adminsortable2.admin import SortableAdminBase
from adminsortable2.admin import SortableInlineAdminMixin

from meetup.forms import MessageForm
from telegram_bot.bot import send_messages_for_all

from .models import Meetup, Participant, Speech, Donation, Questionnaire


class SpeechInline(SortableInlineAdminMixin, admin.TabularInline):
    model = Speech
    fields = [
        'ordinal_number',
        'get_time',
        'time_limit',
        'topic',
        'speaker',
    ]
    readonly_fields = ['get_time', ]
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
    list_filter = ['meetup', ]
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
    list_display = ['tg_id', 'tg_username', 'full_name']
    list_filter = ['meetups', ]
    actions = ['show_form']

    def show_form(self, request, queryset):
        form = MessageForm()
        participant_ids = [user.tg_id for user in queryset]
        return render(request, 'admin/send_message.html', {'form': form, 'queryset': participant_ids})
    show_form.short_description = 'Отправить сообщение'



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


@admin.register(Questionnaire)
class QuestionnaireAdmin(admin.ModelAdmin):
    pass
