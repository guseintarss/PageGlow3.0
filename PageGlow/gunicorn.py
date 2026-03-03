from multiprocessing import cpu_count
from decouple import config

def max_workers():
    return cpu_count()

bind = '0.0.0.0:' + config('PORT', '8000')
max_requests = 1000
worker_class = 'gevent'
workers = max_workers()

env = {
    'DJANGO_SETTINGS_MODULE': 'PageGlow.settings'
}

reload = True
name = 'PageGlow'