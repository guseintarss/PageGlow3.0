# PageGlow 3.0

## Схема управления ограничениями доступа

В проекте используются **два слоя контроля доступа**:

- **Web (Django views/templates)**: доступ к страницам ограничивается на уровне Django (миксины/декораторы).
- **API (Django REST Framework + Djoser/JWT)**: доступ к API ограничивается permission-классами DRF и аутентификацией.

### 1) Web-уровень (страницы)

- **Авторизация для страниц**:
  - Для CBV используется `LoginRequiredMixin` (например, `main.views.AddPage`, `main.views.PostDeleteView`, `users.views.EditProfileUser`).
  - Для FBV используется декоратор `@login_required` (например, `main.views.about`, `users.views.delete_user`).

- **Ограничение “владелец может удалить своё”**:
  - Удаление поста реализовано через `PostDeleteView`, где `get_queryset()` фильтрует записи по текущему пользователю (`author=self.request.user`). Это гарантирует, что пользователь не сможет удалить чужой пост даже при подстановке URL.

### 2) API-уровень (DRF)

- **Глобальная политика доступа по умолчанию** задаётся в `PageGlow/settings.py`:
  - `DEFAULT_PERMISSION_CLASSES = ['rest_framework.permissions.IsAuthenticated']`
  - То есть **любой DRF-эндпоинт по умолчанию требует аутентификации**.

- **Аутентификация для DRF**:
  - Включены `SessionAuthentication` и `BasicAuthentication` (настроено в `REST_FRAMEWORK`).

- **Точечные ограничения для отдельных ресурсов**:
  - `users.views.RuleViewSet` использует `permission_classes = [permissions.IsAdminUser]`, поэтому CRUD по правилам (`/users/rules/...`) доступен **только администратору**.

### 3) Аутентификация и вход (Djoser/JWT + Django)

- **Djoser** подключён в `PageGlow/urls.py`:
  - `path('auth/', include('djoser.urls'))`
  - `path('auth/', include('djoser.urls.jwt'))`
  - Это даёт API для регистрации/входа/сброса пароля и выдачи JWT (формат заголовка `Authorization: Bearer <token>`).

- **Django-сессии** используются для веб-части (обычный логин через `users.views.LoginUser` и стандартные Django views для logout/password reset/password change).

### 4) Где “живут” правила доступа (по структуре проекта)

- **Настройки и дефолтные политики**: `PageGlow/PageGlow/settings.py` (DRF permissions/auth, Djoser, auth backends).
- **Маршрутизация**: `PageGlow/PageGlow/urls.py`, `PageGlow/users/urls.py`.
- **Web-ограничения (страницы)**: `PageGlow/main/views.py`, `PageGlow/users/views.py`.
- **API-ограничения (permissions)**: `PageGlow/users/views.py` (например, `RuleViewSet`).
