from django.core.management.base import BaseCommand
from telegram_bot.bot import main


class Command(BaseCommand):
    help = 'Запуск телеграмм бота'

    def handle(self, *args, **kwargs):
        self.stdout.write("Запуск бота...")
        main()