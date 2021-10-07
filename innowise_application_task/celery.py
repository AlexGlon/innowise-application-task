from __future__ import absolute_import, unicode_literals

import os
from datetime import timedelta

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'innowise_application_task.settings')

app = Celery('celery_tasks')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


# if __name__ == '__main__':
#     app.start()

app.conf.beat_schedule = {
    # 'test_print': {
    #     'task': 'tickets.tasks.test_print',
    #     'schedule': timedelta(seconds=20),
    # },
    'close_old_tickets': {
        'task': 'tickets.tasks.close_old_tickets',
        'schedule': crontab(minute='*/1'),
    },
}
