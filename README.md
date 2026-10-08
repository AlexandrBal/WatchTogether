# Сайт WatchTogether для совместного просмотра видео
## Автор: [AlexandrBal](https://github.com/AlexandrBal)
### Краткое описание

Небольшой учебный pet-проект по работе с FastAPI и SocketIO. Вы можете создавать комнаты, добавляться в них и смотреть видео с друзьями синхронно. Достаточно скопировать ссылку на видео из браузерной поисковой строки и вставить в окно для ссылки. YouTube API сам найдёт нужное видео и запустит его на встроенном проигрывателе.

### Стек технологий

#### Backend

- FastAPI
- Socket.IO
- PostgreSQL
- SQLAlchemy[asyncio]
- Pydantic
- seckrets
- YouTube API

#### Frontend

- HTML
- JavaScript
- CSS

### Версия Python
Python 3.14.7

## Установка

Перед скачиванием зависимостей убедитесь, что вы создвли виртуальное окружение. В противном случае возможен конфликт зависимостей:
`python -m venv .venv`

#### (Linux/macOS)
`source venv/bin/activate`

#### (Windows)
`.venv/Scripts/activate`

Все необходимые зависимости указаны в файле requirements.txt. Чтобы скачать, введите:<br>
`pip install -r requirements.txt`

## Запуск
Находясь в папке проекта, введите в терминале:<br>
`uvicorn backend.main:app --reload`<br>
и перейдите по ссылке. У вас отхроется сайт на локальном сервере.