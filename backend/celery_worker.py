# celery_worker.py

from celery import Celery


# simple config (keep it readable)
celery = Celery(
    "my_app",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

# optional config (not too fancy)
celery.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Kolkata",
    enable_utc=True
)



import tasks