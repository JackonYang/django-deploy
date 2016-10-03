# -*- coding:utf-8 -*-
import os
import sys
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{{ settings }}')

project_dir = '{{ django_root }}'
if project_dir not in sys.path:
    sys.path.append(project_dir)

application = get_wsgi_application()
