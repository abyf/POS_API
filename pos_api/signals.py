from django.core.mail import EmailMessage
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.conf import settings
from django.db.models.signals import post_save
from .models import CardHolder, Merchant, Administrator
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from io import BytesIO
import qrcode
from PIL import Image
from reportlab.lib.pagesizes import letter

def genarete_pdf(model):
    buffer = BytesIO()
    p = canvas.Canvas(buffer,pagesize=letter)

    if isinstance(model,CardHolder):
        p.drawString(100,700,f"Name: {model.name}")
        p.drawString(100,680,f"Phone: {model.phone}")
        p.drawString(100,660,f"Address: {model.address}")
        p.drawString(100,640,f"Alias: {model.alias}")
        #p.drawImage(model.qr_code_img,400,600,100,100)
    elif isinstance(model,Merchant):
        p.drawString(100,700,f"Name: {model.name}")
        p.drawString(100,680,f"Phone: {model.phone}")
        p.drawString(100,660,f"Address: {model.address}")
        p.drawString(100,640,f"Alias: {model.alias}")
        p.drawString(100,640,f"Balance: {model.balance}")
    p.save()
    pdf = buffer.getvalue()
    buffer.close()

    return pdf
@receiver(post_save, sender=CardHolder)
def send_cardholder_email(sender, instance,created,**kwargs):
    if created and instance.email:
        #Generates the cardholder's qr_code image
        qr = qrcode.QRCode(version=1,box_size=10,border=5)
        qr.add_data(str(instance.qr_code))
        qr.make(fit=True)
        img = qr.make_image(fill_color="black",back_color="white")
        buffer = BytesIO()
        img.save(buffer,format='PNG')
        qr_code_file = f'qr_code_{instance.id}.png'
        instance.qr_code_img.save(qr_code_file,buffer)

        #Send email to the newly added cardholder
        subject = 'Welcome to TapNyamoo, Cashless Payment'
        to = [instance.email]
        from_email = settings.EMAIL_HOST_USER
        pdf_file = genarete_pdf(instance)
        email_body = 'Thank you for trusting TapNyamoo, Cashless Payment! Attached, your information.'
        qr_code_path = instance.qr_code_img.path
        with open(qr_code_path,'rb') as f:
            qr_code_data = f.read()

        email = EmailMessage(subject,email_body,from_email,to,)
        email.attach('cardholder_information.pdf',pdf_file,'application/pdf')
        email.attach(qr_code_file,qr_code_data,'image/png')
        email.send()

@receiver(post_save, sender=Merchant)
def send_merchant_email(sender, instance,created,**kwargs):
    if created and instance.email:
        subject = 'Welcome to TapNyamoo, Cashless Payment'
        to = [instance.email]
        from_email = settings.EMAIL_HOST_USER
        pdf_file = genarete_pdf(instance)
        email_body = 'Thank you for trusting TapNyamoo, Cashless Payment! Attached, your information.'

        email = EmailMessage(subject,email_body,from_email,to,)
        email.attach('merchant_information.pdf',pdf_file,'application/pdf')

        email.send()
