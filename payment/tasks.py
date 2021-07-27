from io import BytesIO
from myshop.celery import app
import weasyprint
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from orders.models import Order


@app.task
def payment_completed(order_id):
    order = Order.objects.get(id=order_id)
    subject = f'My Shop - EE Invoice No. {order_id}'
    message = 'Please, Find Attachment the invoice for your recent purchase.'
    email = EmailMessage(subject, message, 'admin@myshop.com', [order.email])
    html = render_to_string('orders/order/pdf.html', {'order': order})
    out = BytesIO()
    stylesheets = [weasyprint.CSS(settings.STATIC_ROOT + 'css/pdf.css')]
    weasyprint.HTML(string=html).write_pdf(out, stylesheets=stylesheets)
    email.attach(f'order_{order.id}.pdf',
                 out.getvalue(),
                 'application/pdf')
    email.send()
