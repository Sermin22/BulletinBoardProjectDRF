# Backend для сайта объявлений

## Описание проекта
Проект представляет собой backend-часть для сайта объявлений, реализованную на **Django + Django REST Framework**.  
Реализован функционал аутентификации, ролей пользователей, CRUD для объявлений и отзывов, поиск, пагинация, а также контейнеризация через Docker.

---

## Функционал

**Аутентификация и авторизация**  
  - JWT (через `djangorestframework-simplejwt`)  
  - Восстановление пароля через email 

Юзер отправляет POST-запрос на адрес /users/reset_password/ с содержанием:
```
{
    "email": "example@mail.com"
}
```
Сервер высылает на почту ссылку вида:
```
"http://localhost:3000/<url>/{uid}/{token}"  # предварительно это настраивается в settings FRONTEND_URL
```

**Пользователи (приложение users, модель CustomUser)**  
  - Роли: `user`, `admin`  
  - Регистрация и авторизация  
  - Профиль с аватаром  

**Объявления (приложение ads, модель Advertisement)**  
  - CRUD-операции  
  - Поиск по названию (через `django-filter`)  
  - Пагинация (по 4 объявления на страницу)  

**Отзывы (приложение ads, модель Comment)**  
  - Возможность оставлять отзывы под объявлениями  
  - CRUD-операции  

**Права доступа (permissions)**  
  - Аноним: только список объявлений  
  - Пользователь: может управлять своими объявлениями и отзывами  
  - Админ: полный доступ ко всем объявлениям и отзывам  

**Docker**  
  - Контейнеризация приложения и PostgreSQL  
  - Готовый `docker-compose.yml`  

**Тестирование**  
  - Покрытие тестами основных функций (`unittest`)  

**Документация API**  
  - Swagger / OpenAPI Docs  
  - Redoc / OpenAPI Docs

---

## Используемый стек

- **Django**  
- **Django ORM**
- **Django REST Framework (DRF)**  
- **PostgreSQL**
- **OpenAPI Docs**
- **Permissions**
- **Readme**
- **Serializers**
- **Tests**
- **Generic**
- **Auth**
- **Docker + Docker Compose**  
- **JWT (Simple JWT)**  
- **Git**  
- **Swagger / drf-yasg**
- **Filter**
- **django-filter**  
- **CORS Headers**  
- **PEP8 (flake8, black)**  

---

## Установка и запуск

### 1. Клонируем репозиторий
```
git clone https://github.com/Sermin22/BulletinBoardProjectDRF.git
```
### 2. Создайте файл .env  
В корне проекта создайте файл .env и укажите необходимые переменные окружения. 

Пример файла - .env_template

### 3. Установить зависимости:

```
pip install -r requirements.txt
```
### 4. Создать базу данных.

### 5. Выполнить миграции:

```
python manage.py migrate
```

### 6. Если запустить локально
```
python manage.py runserver
```

### 7. Запускаем через Docker
Docker должен быть заранее установлен и запущен.
```
docker-compose up -d --build
```
Первый запуск может занять несколько минут, так как будут устанавливаться зависимости, 
применяться миграции и запускаться фоновые процессы.

Проверяем работоспособность контейнеров:
```
docker-compose ps
```
После запуска создайте суперюзера (по желанию):
```
docker-compose exec web python manage.py createsuperuser
```
Вы можете также подключиться к контейнеру для отладки:
```
docker-compose exec web bash
```
### Структура docker-compose

В проекте настроены следующие сервисы:

- web — основной Django-бэкенд

- db — PostgreSQL база данных

### 8. Остановка проекта

Для остановки всех сервисов:
```
docker-compose down
```

Если нужно удалить тома базы данных и кэша:
```
docker-compose down -v
```

## После запуска:

- Бэкенд доступен по адресу: http://localhost:8000

- Swagger-документация: http://localhost:8000/swagger/
- Альтернативная документация: http://localhost:8000/redoc/

## Основные эндпоинты API
### Аутентификация

- POST /api/token/ – получение JWT токена

- POST /api/token/refresh/ – обновление токена

- POST /api/users/reset_password/ – сброс пароля (отправка ссылки на email)

- POST /api/users/reset_password_confirm/ – подтверждение смены пароля

### Пользователи

- POST /api/users/register/ – регистрация

### Объявления

- GET /api/ads/ads/ – список объявлений (+ поиск, пагинация)

- POST /api/ads/create/ – создать объявление

- GET /api/ads/{id}/ – получить объявление

- PUT /api/ads/{id}/update/ – обновить объявление

- DELETE /api/ads/{id}/delete/ – удалить объявление

### Отзывы

- GET /api/ads/comments/ – список отзывов

- POST /api/ads/comments/create/ – создать отзыв

- PUT /api/comments/{id}//update/ – редактировать отзыв

- DELETE /api/comments/{id}//delete/ – удалить отзыв

- POST /api/ads/{id}/comments/ – добавить отзыв

Вложенные пути:

- GET /apiads/{advertisement_id}/comments/ - список комментариев конкретного объявления
- POST /apiads/{advertisement_id}/comments/create/ - добавить комментарий к объявлению

### Тесты

Запуск тестов:
```
python manage.py test
```

## Автор
Sergei, msm2203@mail.ru
```
https://github.com/Sermin22/
```