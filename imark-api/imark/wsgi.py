"""
WSGI config for imark project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

# sys.path.append('/root/anaconda3/envs/imark_env/lib/python3.8/site-packages/')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'imark.settings')

application = get_wsgi_application()
