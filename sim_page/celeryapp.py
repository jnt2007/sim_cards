from __future__ import absolute_import

import os
import sys

from celery import Celery

# set the default Django settings module for the 'celery' program.
sys.path.append('/home/anton/www/sim_site/')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sims.settings')

from django.conf import settings  # noqa

app = Celery('sims')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
app.conf.update(
    CELERY_RESULT_BACKEND='djcelery.backends.database:DatabaseBackend',
)


if __name__ == '__main__':
    app.start()
