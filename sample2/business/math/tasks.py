from __future__ import absolute_import, unicode_literals
from celery import states
from sample2.back import backapp

# -------------- TASK --------------
@backapp.task(bind = True)
def add_task(self, a, b):
    self.update_state(state = states.PENDING)
    return a + b

@backapp.task(bind = True)
def mul_task(self, a, b):
    self.update_state(state = states.PENDING)
    return a * b
