#!/bin/bash
# 🚀 QUICK START GUIDE - PageGlow 3.0.1
# 
# Использование:
#   bash QUICKSTART.sh docker      # Для Docker
#   bash QUICKSTART.sh local       # Для локального развития
#   bash QUICKSTART.sh help        # Справка

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
print_header() {
    echo -e "\n${BLUE}╔════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║ ${1}${NC}"
    echo -e "${BLUE}╚════════════════════════════════════════╝${NC}\n"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

show_help() {
    cat << EOF
${BLUE}PageGlow 3.0.1 - Быстрый старт${NC}

${YELLOW}Использование:${NC}
  bash QUICKSTART.sh docker      Развертывание с Docker
  bash QUICKSTART.sh local       Локальное развитие
  bash QUICKSTART.sh help        Эта справка

${YELLOW}Примеры:${NC}
  # Docker в production
  bash QUICKSTART.sh docker

  # Локальное развитие
  bash QUICKSTART.sh local

${YELLOW}Дополнительно:${NC}
  - Полная документация: FULL_README.md
  - Развертывание: DEPLOYMENT.md
  - Безопасность: SECURITY.md
  - История изменений: CHANGELOG.md
EOF
}

# ===== DOCKER =====
docker_setup() {
    print_header "🐳 DOCKER DEPLOYMENT"

    # Check docker
    if ! command -v docker &> /dev/null; then
        print_error "Docker не установлен"
        echo "Установите Docker с https://docker.com"
        exit 1
    fi

    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose не установлен"
        exit 1
    fi

    print_success "Docker найден"

    # Create .env
    if [ ! -f ".env" ]; then
        print_warning ".env файл не найден, создаю из .env.example"
        cp .env.example .env
        print_warning "📝 Отредактируйте .env с вашими настройками!"
        print_warning "Критичные переменные:"
        echo "  - SECRET_KEY (минимум 50 символов)"
        echo "  - DATABASE_PASSWORD (сильный пароль)"
        echo "  - EMAIL_HOST_USER (ваш email)"
        echo "  - EMAIL_HOST_PASSWORD (app password)"
        echo ""
        print_warning "После редактирования выполните:"
        echo "  docker-compose up -d"
        return
    fi

    print_success ".env файл найден"

    # Start services
    print_header "Запуск контейнеров..."
    docker-compose up -d

    sleep 5

    print_success "Контейнеры запущены"

    # Check status
    print_header "Статус сервисов"
    docker-compose ps

    # Initialize database
    print_header "Инициализация базы данных"
    docker-compose exec -T pageglow python manage.py migrate
    print_success "Миграции выполнены"

    # Create superuser
    print_warning "Создание superuser..."
    docker-compose exec pageglow python manage.py createsuperuser || true

    # Collect static
    print_header "Сбор статических файлов"
    docker-compose exec pageglow python manage.py collectstatic --noinput
    print_success "Статика собрана"

    # Health check
    print_header "Проверка здоровья приложения"
    sleep 5
    HEALTH=$(curl -s http://localhost/health/ || echo "error")
    if echo "$HEALTH" | grep -q "healthy"; then
        print_success "Приложение здорово!"
    else
        print_warning "Проверьте логи: docker-compose logs pageglow"
    fi

    # Summary
    print_header "🎉 Docker развертывание завершено!"
    echo ""
    echo -e "${GREEN}Доступные адреса:${NC}"
    echo "  🌐 Приложение: http://localhost"
    echo "  🔐 Админ-панель: http://localhost/admin"
    echo "  💾 Adminer (БД): http://localhost:8080"
    echo ""
    echo -e "${GREEN}Полезные команды:${NC}"
    echo "  docker-compose logs -f pageglow    # Логи приложения"
    echo "  docker-compose ps                  # Статус сервисов"
    echo "  docker-compose down                # Остановить"
    echo "  docker-compose down -v             # Удалить (включая БД!)"
    echo ""
    echo -e "${YELLOW}Дальше:${NC}"
    echo "  1. Откройте http://localhost в браузере"
    echo "  2. Войдите в админ-панель http://localhost/admin"
    echo "  3. Создавайте статьи и исследуйте платформу"
}

# ===== LOCAL =====
local_setup() {
    print_header "💻 LOCAL DEVELOPMENT"

    # Check Python
    if ! command -v python3 &> /dev/null; then
        print_error "Python3 не установлен"
        echo "Установите Python 3.11+ с https://python.org"
        exit 1
    fi

    PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
    print_success "Python $PYTHON_VERSION найден"

    # Change to PageGlow directory
    cd PageGlow

    # Create venv
    if [ ! -d "venv" ]; then
        print_header "Создание виртуального окружения"
        python3 -m venv venv
        print_success "Виртуальное окружение создано"
    fi

    # Activate venv
    print_header "Активирование venv"
    source venv/bin/activate 2>/dev/null || \
    . venv/Scripts/activate 2>/dev/null || \
    print_warning "Активируйте вручную: source venv/bin/activate"

    # Install requirements
    print_header "Установка зависимостей"
    pip install --upgrade pip
    pip install -r requirements.txt
    print_success "Зависимости установлены"

    # Create .env
    if [ ! -f ".env" ]; then
        print_warning ".env не найден, создаю из .env.example"
        cp ../.env.example .env
        print_success ".env создан (используются значения по умолчанию)"
    fi

    # Migrate
    print_header "Миграция базы данных"
    python manage.py migrate
    print_success "Миграции выполнены"

    # Create superuser
    print_warning "Создание superuser..."
    python manage.py createsuperuser

    # Collect static
    print_header "Сбор статических файлов"
    python manage.py collectstatic --noinput
    print_success "Статика собрана"

    # Summary
    print_header "🎉 Локальное развитие готово!"
    echo ""
    echo -e "${GREEN}Для запуска:${NC}"
    echo "  cd PageGlow"
    echo "  source venv/bin/activate"
    echo "  python manage.py runserver"
    echo ""
    echo -e "${GREEN}Доступ:${NC}"
    echo "  🌐 Приложение: http://localhost:8000"
    echo "  🔐 Админ-панель: http://localhost:8000/admin"
    echo ""
    echo -e "${YELLOW}Полезные команды:${NC}"
    echo "  python manage.py runserver          # Запустить dev сервер"
    echo "  python manage.py shell              # Django shell"
    echo "  python manage.py makemigrations     # Создать миграции"
    echo "  python manage.py test               # Запустить тесты"
    echo ""
    echo -e "${YELLOW}Документация:${NC}"
    echo "  FULL_README.md      - Полное описание"
    echo "  DEPLOYMENT.md       - Развертывание"
    echo "  SECURITY.md         - Безопасность"
}

# ===== MAIN =====
case "${1:-help}" in
    docker)
        docker_setup
        ;;
    local)
        local_setup
        ;;
    help|--help|-h|"")
        show_help
        ;;
    *)
        print_error "Неизвестная команда: $1"
        echo ""
        show_help
        exit 1
        ;;
esac

print_success "Готово! 🚀"
