## Проект Благотворительный фонд поддержки котиков QRKot
 финальное задание 23 спринта

### QRKot реализован с использованием:
  - Django
  - Django Rest Framework
  - Nginx
  - PostgreSQL/SQLite
  - Docker

### Как развернуть проект:

Клонировать репозиторий и перейти в папку бэкенда проекта:
```bash
git clone https://github.com/peskoval/foodgram.git
cd foodgram/backend/
```

Cоздать и активировать виртуальное окружение:
```bash
python3 -m venv venv
source .venv/bin/activate
```

Установить зависимости:
```bash
pip3 install -r requirements.txt
```

##### Для SQLite
```bash
export USE_SQLITE=true
```

##### Для PostgreSQL (по умолчанию)
```bash
unset USE_SQLITE
```

Применение миграций, сборка статики и запуск сервера:
```bash
python3 manage.py migrate
python3 manage.py collectstatic
python3 manage.py runserver
```
Наполнить базу ингредиентами и тегами:
```bash
python3 manage.py load_ingredients ../data/ingredients.json
python3 manage.py load_tags ../data/tags.json

```


#### Запуск проекта в Docker:
Создать файл .env в корне проекта со следующей структурой:
```env
POSTGRES_USER=Имя пользователя для подклчения к базе
POSTGRES_PASSWORD=Пароль пользователя для подключения к базе
POSTGRES_DB=Название базы
DB_HOST=Хост базы данных
DB_PORT=Порт
DB_NAME=Название базы
SECRET_KEY=Секретный ключ для проекта
ALLOWED_HOSTS=Список разрешенных хостов
DEBUG=Режим разработки True/False
```

Запустить Docker Desktop;
Запустить docker-compose:
```bash
docker compose -f docker-compose.production.yml up
```

### Доступные эндпоинты в API

[Панель администрирования](localhost/admin/)
[Ингредиенты](localhost/api/ingredients/)
[Рецепты](localhost/api/recipes/)
[Короткая ссылка на рецепт](localhost/api/recipes/{id}/get-link/)
[Избранные рецепты](localhost/api/recipes/{id}/favorite/)
[Загрузка файла со списком покупок](localhost/api/recipes/download_shopping_cart/)
[Теги](localhost/api/tags/)
[Пользователи](localhost/api/users/)
[Подписки](localhost/api/users/subscriptions/)
[Документация](localhost/api/docs/)

---
Автор: Peskoval (Пескова Александра Олеговна)
[Связь в Telegram](https://t.me/vieuxcamee)