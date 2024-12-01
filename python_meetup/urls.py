from django.contrib import admin
from django.urls import path
from meetup.views import send_message_view

urlpatterns = [
    path('admin/', admin.site.urls),
]
urlpatterns += [
    path('send-messages/', send_message_view, name='send-message'),
]
