from __future__ import absolute_import, unicode_literals
from celery import shared_task
import requests
from .serializers import WebhookSerializer
from .models import Payment

@shared_task(bind=True,max_retries=5, retry_backoff=30)
def payment_update_notification(self,payment_id,payload):
    payment = Payment.objects.get(id=payment_id)
    # Serialize the webhook payload
    serializer = WebhookSerializer(payment)
    serialized_payload = serializer.data
    print(serialized_payload)
    serialized_payload.update(payload)
    print(serialized_payload)
    # Send  the webhook payload to the remote API application
    try:
        response = requests.post('https://abyf.pythonanywhere.com/payment_update',data=serialized_payload,headers={'content-type':'application/json'})
        response.raise_for_status()
    except requests.exceptions.RequestException as exc:
        self.retry(exc=exc)
