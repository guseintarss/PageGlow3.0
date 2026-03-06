# 🔐 Документация по безопасности PageGlow

## Содержание

1. [Обзор](#обзор)
2. [Аутентификация](#аутентификация)
3. [Авторизация](#авторизация)
4. [Защита данных](#защита-данных)
5. [API Security](#api-security)
6. [Производственная безопасность](#производственная-безопасность)

---

## Обзор

PageGlow использует многоуровневую систему безопасности:

- **Transport Security**: HTTPS/TLS
- **Authentication**: Session + JWT
- **Authorization**: Role-based access control (RBAC)
- **Data Protection**: CSRF, XSS, SQL Injection prevention
- **API Security**: Rate limiting, Token-based auth

---

## Аутентификация

### Веб-сессии (Django)

```python
# Вход пользователя через форму
LOGIN_URL = 'users:login'
LOGIN_REDIRECT_URL = 'home'

# Конфигурация сессий
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 1209600  # 2 недели
SESSION_COOKIE_SECURE = True  # Только HTTPS в production
SESSION_COOKIE_HTTPONLY = True  # Недоступно JavaScript
SESSION_COOKIE_SAMESITE = 'Lax'  # CSRF protection
```

### JWT (JSON Web Tokens)

```python
# Для API в production
from rest_framework_simplejwt.tokens import RefreshToken

# Получить токены
refresh = RefreshToken.for_user(user)
access_token = refresh.access_token
```

**Endpoints:**
- `POST /auth/jwt/create/` - Получить токены
- `POST /auth/jwt/refresh/` - Обновить access token
- `POST /auth/jwt/verify/` - Проверить токен

### Пароли

```python
# Django использует PBKDF2 с HMAC-SHA256 по умолчанию
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]

# Требования к паролю (в settings.py)
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]
```

---

## Авторизация

### Role-Based Access Control (RBAC)

#### Уровень Django Views

```python
# Class-Based Views
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    
    def test_func(self):
        # Только автор может удалить свой пост
        return self.get_object().author == self.request.user

# Function-Based Views
from django.contrib.auth.decorators import login_required

@login_required
def profile_view(request):
    # Только для аутентифицированных пользователей
    return render(request, 'profile.html')
```

#### Уровень DRF (API)

```python
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
    BasePermission
)

# Глобальная настройка
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

# Пользовательское разрешение
class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Чтение разрешено всем
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True
        # Запись только для владельца
        return obj.author == request.user

# ViewSet с разрешениями
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        # Только свои посты для редактирования
        if self.action in ['update', 'partial_update', 'destroy']:
            return self.request.user.posts.all()
        return Post.published.all()
```

### Специальные группы прав

```python
# Администраторы
user.is_staff = True
user.is_superuser = True

# Модераторы (кастомные группы)
from django.contrib.auth.models import Group

moderators_group = Group.objects.get(name='Moderators')
user.groups.add(moderators_group)
```

---

## Защита данных

### CSRF Protection

```python
# Включена по умолчанию в settings.py
MIDDLEWARE = [
    # ...
    'django.middleware.csrf.CsrfViewMiddleware',
    # ...
]

# В шаблонах
<form method="post">
    {% csrf_token %}
    <!-- форма здесь -->
</form>

# В AJAX запросах
fetch('/api/endpoint/', {
    method: 'POST',
    headers: {
        'X-CSRFToken': getCookie('csrftoken'),
        'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
})
```

### XSS Prevention

```python
# Django автоматически экранирует переменные в шаблонах
{{ user_input }}  # Автоматически экранируется

# Если нужно вставить HTML - используйте |safe только для trusted content
{{ trusted_html|safe }}

# Для содержимого из редактора - используйте bleach
from bleach import clean

allowed_tags = ['p', 'br', 'strong', 'em', 'a', 'img']
allowed_attrs = {'a': ['href'], 'img': ['src', 'alt']}

safe_html = clean(user_content, tags=allowed_tags, attributes=allowed_attrs)
```

### SQL Injection Prevention

```python
# ✅ ПРАВИЛЬНО - используется ORM
posts = Post.objects.filter(author=request.user)

# ❌ НЕПРАВИЛЬНО - raw SQL
posts = Post.objects.raw(f"SELECT * FROM main_post WHERE author_id={user_id}")

# ❌ НЕПРАВИЛЬНО - string interpolation
Post.objects.filter(title=f"SELECT * FROM {user_input}")
```

### Information Disclosure

```python
# Не отправлять чувствительные ошибки в production
DEBUG = False

# Логировать ошибки, но не показывать пользователю
LOGGING = {
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/pageglow/django.log',
        },
    },
}

# Пользовательские 404/500 страницы (не показывают traceback)
handler404 = 'main.views.page_not_found'
handler500 = 'main.views.server_error'
```

---

## API Security

### Authentication

```python
# JWT Token Format
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# Session Authentication (для веб-интерфейса)
Cookie: sessionid=abc123...
```

### Rate Limiting

```python
# Ограничение количества запросов
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',  # Неавторизованные пользователи
        'user': '1000/hour'  # Авторизованные пользователи
    }
}

# Кастомное throttle
from rest_framework.throttling import UserRateThrottle

class BurstRateThrottle(UserRateThrottle):
    scope = 'burst'

# В settings
'DEFAULT_THROTTLE_RATES': {
    'burst': '100/hour'
}
```

### Input Validation

```python
# Использовать DRF Serializers для валидации
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'category']
    
    def validate_title(self, value):
        if len(value) < 5:
            raise serializers.ValidationError("Title too short")
        return value
    
    def validate(self, data):
        if not data.get('content'):
            raise serializers.ValidationError("Content is required")
        return data
```

### CORS

```python
# Если использовать CORS
CORS_ALLOWED_ORIGINS = [
    "https://your-domain.com",
    "https://www.your-domain.com",
]

CORS_ALLOW_CREDENTIALS = True  # Для cookies
```

---

## Производственная безопасность

### Обязательная конфигурация (django-admin check --deploy)

```python
# ✅ PRODUCTION CHECKLIST

# 1. Отключить DEBUG
DEBUG = False

# 2. Установить SECRET_KEY
SECRET_KEY = 'your-long-random-secret-key-min-50-chars'

# 3. ALLOWED_HOSTS
ALLOWED_HOSTS = ['your-domain.com', 'www.your-domain.com']

# 4. HTTPS
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# 5. HSTS
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# 6. Content Security Policy
SECURE_CONTENT_SECURITY_POLICY = {
    'default-src': ("'self'",),
    'script-src': ("'self'", "cdn.jsdelivr.net"),
    'style-src': ("'self'", "cdn.jsdelivr.net"),
}

# 7. X-Frame-Options
X_FRAME_OPTIONS = 'DENY'

# 8. Безопасные cookies
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_HTTPONLY = True
```

### Docker Security

```dockerfile
# ✅ Хороший Dockerfile
FROM python:3.11-slim

# Создать непривилегированного пользователя
RUN groupadd -r django && useradd -r -g django django

# Установить переменные для безопасности
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Изменить права
RUN chown -R django:django /app

# Использовать непривилегированного пользователя
USER django

EXPOSE 8000
CMD ["gunicorn", "PageGlow.wsgi:application"]
```

### Nginx Security

```nginx
# ✅ Безопасный Nginx конфиг
server {
    listen 443 ssl http2;
    
    # SSL/TLS
    ssl_certificate /etc/letsencrypt/live/domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/domain.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
    
    # Security Headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    add_header Content-Security-Policy "default-src 'self'; script-src 'self' cdn.jsdelivr.net" always;
    
    # Логирование
    access_log /var/log/nginx/pageglow_access.log;
    error_log /var/log/nginx/pageglow_error.log warn;
    
    # Остальная конфигурация...
}
```

### Email Security

```python
# Отправка писем по SMTP с TLS
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 465
EMAIL_USE_SSL = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'app-specific-password'  # НЕ основной пароль!
```

---

## Мониторинг и Auditing

### Логирование действий пользователей

```python
from django.contrib.admin.models import LogEntry

# Просмотр истории действий в админ-панели
# /admin/admin/logentry/

# Кастомное логирование
import logging

logger = logging.getLogger(__name__)

def sensitive_action(request):
    logger.warning(
        f"User {request.user.id} performed sensitive action",
        extra={
            'user_id': request.user.id,
            'ip': get_client_ip(request),
            'timestamp': timezone.now()
        }
    )
```

### Мониторинг безопасности

```bash
# Проверка конфигурации security
python manage.py check --deploy

# Сканирование зависимостей на уязвимости
pip install safety
safety check

# Проверка кода на уязвимости (bandit)
pip install bandit
bandit -r PageGlow/
```

---

## Частые ошибки безопасности

| ❌ Неправильно | ✅ Правильно |
|---|---|
| `DEBUG=True` в production | `DEBUG=False` с логированием |
| Hardcoded SECRET_KEY | Использовать переменные окружения |
| `eval()` или `exec()` | Безопасные парсеры/валидаторы |
| Raw SQL с f-strings | Django ORM с параметрами |
| Сохранять пароли в plain text | Использовать password hashers |
| Доверять user input | Валидировать и экранировать все |
| Отправлять трассировки ошибок | Логировать приватно, показывать generic ошибку |
| Отключить CSRF | Использовать CSRF tokens везде |
| HTTP вместо HTTPS | Требовать HTTPS везде |
| Показывать sensitive data в logs | Маскировать пароли и токены |

---

## Инциденты безопасности

### Если обнаружена уязвимость:

1. **Немедленно** отключить затронутый функционал
2. Оценить масштаб нарушения
3. Уведомить пользователей через email
4. Создать patch и тестировать
5. Развернуть исправление
6. Провести audit
7. Документировать инцидент

### Пример ответа:

```python
# Отключить опасный endpoint
class RiskyViewSet(viewsets.ModelViewSet):
    def create(self, request, *args, **kwargs):
        logger.critical("SECURITY: Exploit attempt detected")
        return Response(
            {"detail": "This feature is temporarily disabled"},
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )
```

---

## Ресурсы

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Django Security](https://docs.djangoproject.com/en/6.0/topics/security/)
- [DRF Permissions](https://www.django-rest-framework.org/api-guide/permissions/)
- [CWE/SANS Top 25](https://cwe.mitre.org/top25/)

---

**Документ последний раз обновлен: March 5, 2026**
