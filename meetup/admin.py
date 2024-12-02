from datetime import timedelta
from django.contrib import admin
from django.shortcuts import render

from adminsortable2.admin import SortableAdminBase
from adminsortable2.admin import SortableInlineAdminMixin

from meetup.forms import MessageForm

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
        if obj.ordinal_number == 1:
            return f'{format(date,"%H:%M")} - {format(date + timedelta(minutes=obj.time_limit), "%H:%M")}'
        return f'{format(date + timedelta(minutes=5),"%H:%M")} - {format(date + timedelta(minutes=obj.time_limit), "%H:%M")}'
        
    get_time.short_description = 'Слот'


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
    list_filter = ['meetup',]


@admin.register(Questionnaire)
class QuestionnaireAdmin(admin.ModelAdmin):
    pass
