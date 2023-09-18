# Проект Foodgram
Foodgram - это онлайн-сервис, где пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов в формате txt, необходимых для приготовления одного или нескольких выбранных блюд.

Дипломный проект курса Python-разработчик от Яндекс.Практикум.

### Стек технологий:
Стек: Python, Django 4.2, DRF, PostgreSQL, Docker, nginx, gunicorn.

### Функционал
Незарегистрированные пользователи могут:
- Создать аккаунт
- Просматривать рецепты на главной
- Просматривать отдельные страницы рецептов
- Просматривать страницы пользователей
- Фильтровать рецепты по тегам

Авторизованные пользователи могут то же, что и незарегистрированные, плюс:

- Создавать/редактировать/удалять собственные рецепты
- Работать с персональным списком избранного: добавлять в него рецепты или удалять их, просматривать свою страницу избранных рецептов.
- Работать с персональным списком покупок: добавлять/удалять любые рецепты, выгружать файл с количеством необходимых ингредиентов для рецептов из списка покупок.
- Подписываться на публикации авторов рецептов и отменять подписку, просматривать свою страницу подписок.

## Развертывание проекта локально
-  Клонируем репозиторий с проектом:
```
git clone https://github.com/PressXToWin/foodgram.git
```
-  В папке с проектом создаем и активируем виртуальное окружение:
```
python -m venv venv
source venv/scripts/activate
```
-  Устанавливаем зависимости:
```
cd backend
python -m pip install --upgrade pip
pip install -r requirements.txt
```
-  Создаем .env файл в директории infra/, в котором должны содержаться следующие переменные:
```
DB_NAME=foodgram
POSTGRES_USER=foodgram
POSTGRES_PASSWORD=password
DB_HOST=db
DB_PORT=5432

SECRET_KEY=321
DEBUG=True
ALLOWED_HOSTS=127.0.0.1
CSRF_TRUSTED_ORIGINS=http://127.0.0.1

```
-  Создаем и запускаем контейнеры Docker:
```
docker compose up -d
```

-  После успешного запуска контейнеров наполним бд и создаим суперюзера:
```
docker compose exec backend python manage.py load_csv
docker compose exec backend python manage.py createsuperuser
```
Проект доступен по адресу:
```
http://localhost/
```

## Развертывание проекта на удаленном сервере
 - Склонируйте репозиторий. 
```
https://github.com/PressXToWin/foodgram.git
```
 - Создайте .env файл в директории infra/, в котором должны содержаться следующие переменные для подключения к базе PostgreSQL:
```
DB_NAME=foodgram
POSTGRES_USER=foodgram
POSTGRES_PASSWORD=password
DB_HOST=db
DB_PORT=5432

SECRET_KEY=321
DEBUG=True
ALLOWED_HOSTS=127.0.0.1 yourdomain.com
CSRF_TRUSTED_ORIGINS=http://127.0.0.1 https://yourdomain.com
```
 - Скопируйте на сервер файлы docker-compose.yml, nginx.conf из папки infra (команды выполнять находясь в папке infra):
```
scp docker-compose.yml nginx.conf username@IP:/home/username/
```
 - Создайте и запустите контейнеры Docker, выполнив команду на сервере:
```
docker compose up -d
```
 - После успешной сборки нужно наполнить базу, создать суперпользователя:
```
docker compose exec backend python manage.py load_csv
docker compose exec backend python manage.py createsuperuser
```
