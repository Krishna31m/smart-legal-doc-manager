from .celery_worker import celery
from .notification import is_significant_change, send_notification

@celery.task
def check_change(old_text, new_text, doc_id):

    if is_significant_change(old_text, new_text):

        send_notification(doc_id)