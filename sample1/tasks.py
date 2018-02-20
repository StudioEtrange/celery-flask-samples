from __future__ import absolute_import, unicode_literals
from celery import states
from sample1.back import backapp

# -------------- TASK --------------
@backapp.task(bind = True)
def add_task(self, a, b):
    return a + b

@backapp.task(bind = True)
def mul_task(self, a, b):
    return a * b
