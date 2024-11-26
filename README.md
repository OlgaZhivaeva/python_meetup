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
ALLOWED_HOSTS=список хостов
```

Создайте файл базы данных и сразу примените все миграции командой
```python
python3 manage.py migrate
```
Запустите сервер командой
```python
python3 manage.py runserver
```