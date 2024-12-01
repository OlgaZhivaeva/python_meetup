# Python meetup

Приложение для организации митапов

### Как установить

Python3 должен быть уже установлен. Затем используйте `pip` (или `pip3`, есть конфликт с Python2) для установки зависимостей:

Скачайте код. Перейдите в папку проекта `python_meetup`.

Установите и активируйте виртуальное окружение
```commandline
python3 -m venv venv
source venv/bin/activate
```
Установите зависимости командой
```commandline
pip install -r requirements.txt
```
В каталоге проекта создайте файл `.env` и поместите в него переменные окружения
```commandline
TG_BOT_TOKEN=ваш токен телеграмм бота
SECRET_KEY=ваш секретный ключ джанго проекта
DEBUG=True или False
```

Создайте файл базы данных и сразу примените все миграции командой
```python
python3 manage.py migrate
```

При необходимости заполните базу данных тестовыми данным
```python
python manage.py fill_db_by_test_data
```

Запустите сервер командой в одном терминале
```python
python3 manage.py runserver
```

Запустите бота командой в другом терминале
```python
python3 manage.py run_bot
```

### Примеры работы



### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).
