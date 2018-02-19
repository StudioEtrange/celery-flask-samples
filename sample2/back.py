from __future__ import absolute_import, unicode_literals
import os
from celery import Celery




backapp = Celery('sample2',
             broker=os.environ['CELERY_BROKER_URL'],
             backend=os.environ['CELERY_RESULT_BACKEND'],
             include=['sample2.business.math.tasks'])

#backapp.conf.update(frontapp.config)

backapp.conf.update(
    # enable STARTED status for celery task
    # needed to know if a task exists
    task_track_started=True,
    #result_expires=3600,
)

if __name__ == '__main__':
    backapp.start()
