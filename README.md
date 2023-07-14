# Проект Foodgram
Foodgram - продуктовый помощник с базой кулинарных рецептов. Пользователям предоставлена возможность просмотра опубликованных рецептов и публикации собственных. Доступна возможность подписки на авторов, добавление рецептов в избранное,  а так же скачивание списка покупок.
  
### Стек технологий:
Стек: Python 3.7, Django, DRF, PostgreSQL, Docker, nginx, gunicorn.

# Развертывание проекта локально
-  Клонируем репозиторий с проектом:
```
git clone https://github.com/PressXToWin/foodgram-project-react.git
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

# Развертывание проекта на удаленном сервере
 - Склонируйте репозиторий. 
```
https://github.com/PressXToWin/foodgram-project-react.git
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
 - Скопировать на сервер файлы docker-compose.yml, nginx.conf из папки infra (команды выполнять находясь в папке infra):
```
scp docker-compose.yml nginx.conf username@IP:/home/username/
```
 - Создать и запустить контейнеры Docker, выполнить команду на сервере:
```
docker compose up -d
```
 - После успешной сборки выполнить миграции, собрать статику, наполнить базу, создать суперпользователя:
```
docker compose exec backend python manage.py load_csv
docker compose exec backend python manage.py createsuperuser
```

# Данные для доступа

url: https://foodgram.yc.pressxtowin.top/signin

user: admin

email: admin@example.com

password: BmVZ5bKQAFxwa4SEybWy