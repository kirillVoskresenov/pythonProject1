from celery import shared_task

def send_mail():
    print("Sending")

import time

@shared_task
def hello():
    time.sleep(10)
    print("Hello, world!")