import os
import django
from wsgiref.simple_server import make_server
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
django.setup()

def run_server():
    application = get_wsgi_application()
    server = make_server("127.0.0.1", 8000, application)
    server.serve_forever()