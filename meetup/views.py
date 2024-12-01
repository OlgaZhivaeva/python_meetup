from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import MessageForm
from telegram_bot.bot import send_messages_for_all
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def send_message_view(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data['message']
            participant_ids = request.POST.getlist('participant_ids')[0].split(',')
            send_messages_for_all(participant_ids, message)
            return HttpResponseRedirect('/admin/')
    else:
        form = MessageForm()
    return render(request, 'admin/send_message.html', {'form': form})
