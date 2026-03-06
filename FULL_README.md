# 📚 PageGlow 3.0.1 - Платформа для блогеров

[![Django](https://img.shields.io/badge/Django-6.0.2-green)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.11+-blue)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue)](https://www.docker.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16+-blue)](https://www.postgresql.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

## 🎯 Описание

**PageGlow** - это современная веб-платформа для создания и публикации статей/блогов с поддержкой:

- 📝 Создания и редактирования статей с расширенным редактором (CKEditor 5)
- 👥 Системы подписок на авторов
- ❤️ Лайков и избранного
- 💬 Комментирования статей
- 🔔 Уведомлений о новых постах
- 🌙 Темной темы/светлого режима
- 🔐 Аутентификации и авторизации
- 📱 Адаптивного дизайна (Mobile-First)
- 🚀 API с DRF и JWT
- ⚡ Кэширования (Redis/File)
- 🐳 Полной Dockerизации

## 📋 Требования

- **Python 3.11+**
- **Docker** и **Docker Compose** (для развертывания)
- **PostgreSQL 16+** (для production)
- **Redis 7+** (опционально, для улучшенного кэширования)

## 🚀 Быстрый старт

### Локальное развертывание

#### 1. Клонирование репозитория

```bash
git clone https://github.com/guseintarss/PageGlow3.0.git
cd PageGlow3.0
```

#### 2. Создание виртуального окружения

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

#### 3. Установка зависимостей

```bash
cd PageGlow
pip install --upgrade pip
pip install -r requirements.txt
```

#### 4. Конфигурация окружения

Скопируйте и отредактируйте файл `.env`:

```bash
cp .env.example .env
```

**Основные переменные в `.env`:**

```ini
# Django
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

# Email (для отправки писем)
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

#### 5. Подготовка базы данных

```bash
cd PageGlow
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic
```

#### 6. Запуск приложения

```bash
python manage.py runserver
```

Приложение доступно: **http://localhost:8000**  
Админ-панель: **http://localhost:8000/admin**

---

## 🐳 Развертывание с Docker

### 1. Создайте `.env` файл

```bash
cp .env.example .env
```

**Заполните переменные:**

```ini
# Django Settings
DEBUG=False
SECRET_KEY=your-super-secret-key-change-this
ALLOWED_HOSTS=localhost,127.0.0.1,pageglow.ru,www.pageglow.ru

# Database
DATABASE_HOST=postgres
DATABASE_PORT=5432
DATABASE_NAME=pageglow_db
DATABASE_USERNAME=postgres
DATABASE_PASSWORD=your-strong-password

# Email
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-specific-password

# Cache & Gunicorn
REDIS_URL=redis://redis:6379/0
CACHE_BACKEND=redis
GUNICORN_WORKERS=4
```

### 2. Запуск контейнеров

```bash
# Запустить все сервисы в фоне
docker-compose up -d

# Инициализация БД
docker-compose exec pageglow python manage.py migrate
docker-compose exec pageglow python manage.py createsuperuser

# Просмотр логов
docker-compose logs -f pageglow

# Остановка
docker-compose down
```

**Сервисы будут доступны:**
- Приложение: **http://localhost**
- Админ-панель: **http://localhost/admin**
- Adminer (БД): **http://localhost:8080**

---

## 📦 Структура проекта

```
PageGlow3.0/
├── PageGlow/
│   ├── main/                 # Основное приложение
│   │   ├── models.py         # Post, Category, Comment
│   │   ├── views.py          # Views и API
│   │   ├── serializers.py    # DRF сериализаторы
│   │   ├── urls.py           # URL маршруты
│   │   └── templates/        # HTML шаблоны
│   │
│   ├── users/                # Приложение пользователей
│   │   ├── models.py         # User модель
│   │   ├── views.py          # Авторизация
│   │   └── serializers.py    # DRF сериализаторы
│   │
│   ├── PageGlow/             # Конфиг проекта
│   │   ├── settings.py       # Основные настройки
│   │   ├── urls.py           # Главные маршруты
│   │   └── wsgi.py           # WSGI конфиг
│   │
│   ├── static/               # CSS, JS, images
│   ├── media/                # Пользовательские файлы
│   ├── templates/            # Базовые шаблоны
│   ├── Dockerfile            # Docker конфиг
│   ├── gunicorn_config.py    # Gunicorn настройки
│   └── requirements.txt       # Python зависимости
│
├── nginx/
│   └── pageglow.conf         # Nginx конфигурация
│
├── compose.yml               # Docker Compose
├── .env.example              # Пример переменных
└── README.md                 # Документация
```

---

## 🔧 Конфигурация

### Основные файлы конфигурации

#### `PageGlow/settings.py`

```python
# Безопасность
DEBUG = False
SECRET_KEY = 'ваш-секретный-ключ'
ALLOWED_HOSTS = ['pageglow.ru', 'www.pageglow.ru']

# База данных - PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'pageglow_db',
        'HOST': 'postgres',  # имя сервиса в docker-compose
        'PORT': '5432',
    }
}

# Кэширование - Redis
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://redis:6379/0',
    }
}
```

#### `PageGlow/gunicorn_config.py`

```python
workers = 4              # Рабочие процессы
worker_class = 'sync'   # Тип рабочего
bind = '0.0.0.0:8000'   # IP и порт
timeout = 30            # Таймаут
max_requests = 1000     # Макс. запросов на рабочего
```

#### `nginx/pageglow.conf`

```nginx
# Проксирование на Django
location / {
    proxy_pass http://pageglow:8000;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
}

# Статика с кэшем
location /static/ {
    alias /app/staticfiles/;
    expires 30d;
}

# Медиа файлы
location /media/ {
    alias /app/media/;
    expires 7d;
}
```

---

## 🔐 Безопасность

### Включенные меры:

✅ **HTTPS/TLS** - конфигурируется в Nginx  
✅ **CSRF Protection** - встроенная защита Django  
✅ **XSS Prevention** - auto-escaping в шаблонах  
✅ **SQL Injection Prevention** - через Django ORM  
✅ **Secure Headers** - X-Frame-Options, CSP и т.д.  
✅ **Password Hashing** - PBKDF2  
✅ **Session Security** - Secure, HttpOnly, SameSite  
✅ **Rate Limiting** - для API endpoints  
✅ **Непривилегированный пользователь** - в Docker  

### Для production:

```bash
# Проверка настроек
python manage.py check --deploy

# Обязательно:
# 1. Изменить SECRET_KEY
# 2. Установить DEBUG=False
# 3. Добавить домены в ALLOWED_HOSTS
# 4. Установить SSL сертификаты
# 5. Настроить Email
# 6. Создать superuser
```

---

## 📊 Производительность

### Оптимизации:

- ✅ **select_related()** / **prefetch_related()** в queries
- ✅ **Redis кэширование** для быстрого доступа
- ✅ **Gunicorn** с несколькими workers
- ✅ **Nginx** как reverse proxy и static server
- ✅ **Database connection pooling**
- ✅ **GZIP компрессия**
- ✅ **Browser caching** через Cache-Control
- ✅ **CDN ready** для статики

### Мониторинг:

```bash
# Health check
curl http://localhost:8000/health/

# Docker статистика
docker stats pageglow-app

# Логи
docker-compose logs -f pageglow
```

---

## 🔄 Управление доступом

### Web-уровень (Django)
- `LoginRequiredMixin` для Class-Based Views
- `@login_required` для Function-Based Views
- Проверка прав собственности

### API-уровень (DRF)
- `IsAuthenticated` permission по умолчанию
- `IsAdminUser` для админ endpoints
- JWT аутентификация

**Детальнее в файле `SECURITY.md`**

---

## 🐛 Найденные и исправленные ошибки

### ❌ → ✅ Исправлено:

| Проблема | Причина | Решение |
|----------|---------|--------|
| `from venv import logger` | Неправильный импорт | `import logging` |
| Dockerfile `grupadd` | Опечатка | `groupadd` |
| Python 3.14.3 | Версия не существует | Python 3.11 |
| Hardcoded пути | Непортативно | Относительные пути |
| DEBUG как string | Ошибка типа | Boolean с config() |
| Отсутствует Redis конфиг | Неполная конфигурация | Добавлена поддержка Redis |
| Неправильная тема | Toggle не работает правильно | Исправлено переключение |
| Старый compose.yml | Устаревший синтаксис | Версия 3.9 + health checks |
| Плохой Nginx конфиг | Неправильные пути | Полная переработка |

---

## 🚢 Развертывание на сервер

### Вариант 1: Docker (Рекомендуется)

```bash
# На сервере
git clone https://github.com/guseintarss/PageGlow3.0.git
cd PageGlow3.0

# Скопировать и отредактировать .env
cp .env.example .env
nano .env  # добавить реальные значения

# Запустить
docker-compose up -d

# Инициализация
docker-compose exec pageglow python manage.py migrate
docker-compose exec pageglow python manage.py createsuperuser
```

### Вариант 2: Ubuntu/Debian (Традиционно)

```bash
# Установка зависимостей
sudo apt-get update
sudo apt-get install python3.11 python3-pip postgresql nginx

# Клон проекта
git clone https://github.com/guseintarss/PageGlow3.0.git
cd PageGlow3.0/PageGlow

# Окружение
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Systemd сервис для Gunicorn (см. документацию)
```

---

## 🐛 Решение проблем

### Контейнер не стартует

```bash
docker-compose logs pageglow  # Посмотреть логи
docker-compose build --no-cache  # Перестроить
docker-compose up -d  # Запустить
```

### Проблемы с БД

```bash
# Переподключение
docker-compose exec pageglow python manage.py migrate

# Дамп БД
docker-compose exec postgres pg_dump -U postgres pageglow_db > backup.sql

# Восстановление
docker-compose exec -T postgres psql -U postgres pageglow_db < backup.sql
```

### Статика не загружается

```bash
docker-compose exec pageglow python manage.py collectstatic --noinput
docker-compose restart nginx
```

### 502 Bad Gateway

```bash
docker-compose logs nginx        # Проверить логи Nginx
docker-compose ps pageglow       # Статус сервиса
docker-compose restart pageglow  # Перезагрузить
```

---

## 📝 API Документация

### Основные endpoints:

```
GET  /health/              # Health check
GET  /api/posts/           # Список постов
POST /api/posts/           # Создать пост (auth)
GET  /post/<slug>/         # Детали поста

POST /auth/users/          # Регистрация
POST /auth/jwt/create/     # Получить JWT токен
GET  /api/users/<id>/      # Профиль пользователя
```

### JWT Аутентификация

```bash
# 1. Получить токен
curl -X POST http://localhost:8000/auth/jwt/create/ \
  -H "Content-Type: application/json" \
  -d '{"username":"user","password":"pass"}'

# 2. Использовать в запросах
curl http://localhost:8000/api/posts/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## 📞 Контакты

- 🐙 **GitHub**: [guseintarss/PageGlow3.0](https://github.com/guseintarss/PageGlow3.0)
- 📧 **Email**: pageglow3@gmail.com
- 💬 **Telegram**: [@pageglow](https://t.me/pageglow)
- 📘 **VK**: [vk.com/pageglow](https://vk.com/pageglow)

---

## 📄 Лицензия

MIT License - свободное использование в личных и коммерческих проектах

---

**Последнее обновление**: March 5, 2026  
**Версия**: 3.0.1
