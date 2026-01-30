## Проект Благотворительный фонд поддержки котиков QRKot
 финальное задание 23 спринта

### QRKot реализован с использованием:
  - FstAPI

### Как развернуть проект:

Клонировать репозиторий и перейти в папку бэкенда проекта:
```bash
git clone https://github.com/peskoval/cat-charity-1.git
cd cat-charity-1
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

#### Запуск проекта:
Создать файл .env в корне проекта со следующей структурой:
```.env
APP_TITLE='Благотворительный фонд поддержки котиков QRKot'
APP_DESCRIPTION='Сервис для поддержки котиков'
DATABASE_URL=sqlite+aiosqlite:///./fastapi.db 
```

Запустить проект:
```bash
uvicorn app.main:app --reload
```

---
Автор: Peskoval (Пескова Александра Олеговна)
[Связь в Telegram](https://t.me/vieuxcamee)