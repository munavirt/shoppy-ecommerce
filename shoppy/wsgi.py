"""
WSGI config for shoppy project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shoppy.settings')

application = get_wsgi_application()

<<<<<<< HEAD

=======
app = application
>>>>>>> 2706546bd0fbc3087bded44572a88ac005627f40
