# migrate.py
import os
from django.core.management import execute_from_command_line

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'towers.settings')
execute_from_command_line(['manage.py', 'migrate'])
