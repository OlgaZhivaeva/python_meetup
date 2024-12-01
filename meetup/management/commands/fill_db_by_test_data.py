from django.core.management.base import BaseCommand
from django.db import transaction
from meetup.models import Participant, Meetup, Donation, Speech, Questionnaire
from datetime import datetime, timedelta
import random


FULL_NAMES = [
    "Иван Иванов", "Анна Смирнова", "Дмитрий Петров", "Екатерина Новикова",
    "Алексей Соколов", "Мария Кузнецова", "Сергей Морозов", "Ольга Волкова",
    "Андрей Зайцев", "Елена Попова", "Николай Лебедев", "Татьяна Семенова",
    "Александр Козлов", "Наталья Давыдова", "Владимир Алексеев", "Юлия Егорова",
    "Михаил Павлов", "Светлана Николаева", "Роман Орлов", "Виктория Фомина",
    "Евгений Степанов", "Марина Григорьева", "Кирилл Ларионов", "Валерия Макарова",
    "Максим Федоров", "Анастасия Воробьева", "Павел Сорокин", "Елизавета Миронова",
    "Григорий Яковлев", "Кристина Киселева", "Денис Григорьев", "Валентина Романова",
    "Артем Кудрявцев", "Алина Максимова", "Тимур Беляев", "Полина Соловьева",
    "Даниил Комаров", "Вероника Андреева", "Илья Борисов", "Дарья Кузьмина"
]

TECHNOLOGIES = [
    "Python, Django, Flask", "JavaScript, React, Node.js", "Java, Spring",
    "C#, .NET", "Ruby, Ruby on Rails", "PHP, Laravel", "Go, Kubernetes",
    "Swift, iOS", "Kotlin, Android", "C++, Game Development", "Data Science, Machine Learning",
    "DevOps, Docker, Kubernetes", "Cybersecurity, Ethical Hacking", "Frontend, HTML, CSS, JavaScript",
    "Backend, Python, Django", "Fullstack, JavaScript, Node.js, React"
]

MEETUPS = [
    {
        "title": "Митап по Python",
        "address": "Москва, ул. Ленина, д. 10"
    },
    {
        "title": "Конференция по Data Science",
        "address": "Санкт-Петербург, Невский проспект, д. 20"
    },
    {
        "title": "Встреча разработчиков Django",
        "address": "Казань, ул. Баумана, д. 30"
    }

]

SPEECH_TOPICS = [
    "Введение в Python", "Машинное обучение для начинающих", "Оптимизация запросов в Django",
    "Работа с API в Django", "Создание нейронных сетей", "Тестирование в Django",
    "Работа с базами данных", "Микросервисы на Python", "DevOps для разработчиков",
    "Кибербезопасность в Python", "Анализ данных с использованием Pandas",
    "Визуализация данных с Matplotlib", "Работа с большими данными",
    "Интеграция с внешними сервисами", "Разработка мобильных приложений на Python"
]


class Command(BaseCommand):
    help = 'Заполнить базу данных тестовыми данными'

    def handle(self, *args, **kwargs):
        with transaction.atomic():
            participants = []
            for i, name in enumerate(FULL_NAMES, start=1):
                participant = Participant.objects.create(
                    tg_id=i,
                    tg_username=f'@user{i}',
                    full_name=name
                )
                participants.append(participant)
            meetups = []
            for i, meetup in enumerate(MEETUPS):
                meetup_db = Meetup.objects.create(
                    title=meetup.get('title'),
                    date=datetime.now() + timedelta(days=i*7),
                    address=meetup.get('address')
                )
                meetups.append(meetup_db)
            for meetup in meetups:
                meetup_participants = random.sample(participants, 15)
                meetup.participants.add(*meetup_participants)
                for i in range(1, 6):
                    speaker = random.choice(meetup.participants.all())
                    Speech.objects.create(
                        speaker=speaker,
                        topic=random.choice(SPEECH_TOPICS),
                        ordinal_number=i,
                        time_limit=random.randint(30, 120),
                        meetup=meetup
                    )
                for participant in meetup_participants:
                    is_communicative_temp = random.choice([True, False])
                    if not is_communicative_temp:
                        continue
                    Questionnaire.objects.create(
                        bio=f'Биография для {participant.full_name}',
                        stack=random.choice(TECHNOLOGIES),
                        meetup=meetup,
                        participant=participant
                    )
            for _ in range(30):
                meetup = random.choice(meetups)
                donor = random.choice(meetup.participants.all())
                Donation.objects.create(
                    meetup=meetup,
                    donor=donor,
                    amount=random.randint(500, 5000)
                )

            self.stdout.write(self.style.SUCCESS(
                'База данных заполнена тестовыми данными.'
            ))
