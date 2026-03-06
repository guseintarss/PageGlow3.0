#!/bin/bash
# Initialization script for PageGlow application
# Usage: ./init.sh

set -e

echo "🚀 Initializing PageGlow..."

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if .env exists
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚠️  .env file not found. Creating from .env.example...${NC}"
    cp .env.example .env
    echo -e "${YELLOW}📝 Please edit .env file with your settings!${NC}"
    exit 1
fi

echo -e "${GREEN}✅ .env file found${NC}"

# Change to PageGlow directory
cd PageGlow

# Run migrations
echo -e "${YELLOW}📊 Running database migrations...${NC}"
python manage.py migrate

# Create superuser if needed
echo -e "${YELLOW}👤 Create superuser...${NC}"
python manage.py createsuperuser --noinput || true

# Collect static files
echo -e "${YELLOW}📦 Collecting static files...${NC}"
python manage.py collectstatic --noinput

# Create necessary directories
echo -e "${YELLOW}📁 Creating necessary directories...${NC}"
mkdir -p logs
mkdir -p cache
mkdir -p media

echo -e "${GREEN}✅ Initialization complete!${NC}"
echo -e "${GREEN}🎉 You can now run: python manage.py runserver${NC}"
