from __future__ import absolute_import, unicode_literals
import os
from celery import Celery




backapp = Celery('sample1',
             broker=os.environ['CELERY_BROKER_URL'],
             backend=os.environ['CELERY_RESULT_BACKEND'],
             include=['sample1.tasks'])

#backapp.conf.update(frontapp.config)

#backapp.conf.update(
#    result_expires=3600,
#)

if __name__ == '__main__':
    backapp.start()
