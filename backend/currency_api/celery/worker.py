import os

from celery import Celery
from celery.schedules import crontab

celery = Celery(
    __name__,
    broker=os.environ['CELERY_BROKER_URL'],
    include=['backend.currency_api.celery.tasks']
)

celery.conf.beat_schedule = {
    'parse_cbr-every-24': {
        'task': 'backend.currency_api.celery.tasks.parse_cbr',
        'schedule': crontab(hour='*/24'),
        'args': ()
    },
    'populate_db-every-12': {
        'task': 'backend.currency_api.celery.tasks.populate_db',
        'schedule': crontab(hour='*/12'),
        'args': ()
    },
}
