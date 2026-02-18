import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
# Указываем путь до manage.py
sys.path.append(os.path.dirname(__file__) + "pageglow/PageGlow3.0/PageGlow")
# Указываем путь до settings.py
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PageGlow.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()