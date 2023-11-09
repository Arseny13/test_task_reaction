## Описание

Требуется разработать простое API приложения на Django REST Framework, для работы с которым используются 4 API endpoints по принципу CRUD.

Допустим это будет личный блог, с одной моделью у которой есть поля: пользователь, имя записи, текст, дата создания, опубликована ли запись.

Важно: не использовать ModelViewSet и viewsets,  допускается использование generics APIView, но в приоритете базовое APIView.

Желательно, но не обязательно:
1. Предусмотреть права, чтобы только пользователь или администратор мог удалять или изменять запись.
2. Написать тесты для разработанного API.
3. Добавить OpenAPI описание с помощью drf-spectacular.

Стэк: python 3.8 и выше, база данных на свое усмотрение.

Срок выполнения тестового задания - 3 дня.


## Переменные окружения (.env)

Создать файл .env
```
touch .env
```
Заполнить по аналогии с .env.example


## Запуск проекта

* Создать виртуальное окружение и активировать его
* Установить зависимости
```
sudo apt install python3.10-venv
python3.10 -m vevn venv
source venv/bin/activate
pip install -r requirements.txt
```
Или установить [pipenv](https://pipenv.pypa.io/en/latest/)
```
$ pip install --user pipenv
```
* Проверить установку
```
$ pipenv --version
pipenv, version 2023.10.24
```

* Выбрать какуб бд использовать( в app/app/settings.py найти строчку DATABASES и закоментить нужное)

* Если выбрали postgres, то надо создать базу данных в postgres

```
sudo apt install postgresql postgresql-contrib -y
sudo -u postgres psql
CREATE DATABASE blog;
CREATE USER blog_user WITH ENCRYPTED PASSWORD 'xxxyyyzzz';  
GRANT ALL PRIVILEGES ON DATABASE blog TO blog_user; 
exit
```
 

* Перейти в папку app и активировать pipenv
```
cd app
pipenv sync
pipenv shell
```

* Cделать миграции, суперпользователя(пожеланию), запустить сервер Django
```
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

* Для заполнения или обновления базы данных исползовать http://127.0.0.1:8000/admin
* Api-документация расположена http://127.0.0.1:8000/api/docs/

## Тесты
* Переключите бд на sqlite
* Запустите тесты
```
pytest
```