# Coursework6

1. Клонирование проекта
Зайти в терминал
С помощью команды cd перейти в директорию, где будет находиться проект.
Склонировать проект
git clone https://github.com/nvLast86/Coursework6.git

2. Настройка виртуального окружения
Создать виртуальное окружение
python3 -m venv venv
Активировать виртуальное окружение
source venv/bin/activate

3. Установка зависимостей
Перейти в каталог проекта и установить зависимости проекта из файла requirements.txt
pip install -r requirements.txt

4. Установка и настройка Redis
Установить
brew install redis
Запустить
redis-server

5. Установка и настройка PostgreSQL
Установить PostreSQL
brew install postgres
Подключиться к PostgreSQL от имени пользователя postgres
psql -U postgres 
Создать базу данных mailings
CREATE DATABASE mailings;
Выйти
\q

6. Настройка окружения
   В директории проекте создать файл .env

   Записать в файл следующие настройки

   EMAIL_HOST_USER=адрес электронной почты для аутенфикации на почтовом сервере
   EMAIL_HOST_PASSWORD=пароль для аутенфикации на почтовом сервере

   DB_USER=имя пользователя (postgres)
   DB_NAME=название базы данных (mailing)
   SECRET_KEY=секретный ключ 
   *В проекте есть шаблон файла .env - .env_exaple

7. Применение миграций
Выполнить команду
python manage.py migrate

8. Заполнение базы данных
Добавить посты
python manage.py add_posts
Создать суперпользователя
python manage.py csu

9. Запуск celery
Открыть новое окно терминала

Из каталога проекта запустить celery командой

celery -A config.celery worker --loglevel=info --pool=solo

10. Запуск сервера Django
Открыть новое окно терминала

Запустить сервер

python manage.py runserver

11. Работа с приложением
Зарегистрироваться
Перейти по ссылке, отправленной на электронную почту
Создать клиентов
Создать сообщение
Создать рассылку
