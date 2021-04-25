from decimal import Decimal
from django.conf import settings
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from paypal.standard.forms import PayPalPaymentsForm
from django.http import HttpResponse
from django.template.loader import render_to_string
import weasyprint
from orders.models import Order
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def payment_done(request):
    return render(request, 'payment/done.html')

@csrf_exempt
def payment_canceled(request):
    return render(request, 'payment/canceled.html')


def payment_process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    '''host = request.get_host()

    paypal_dict = {
            'business': settings.PAYPAL_RECEIVER_EMAIL,
            'amount': '%.2f' % order.get_total_cost().quantize(Decimal('.01')),
            'item_name': 'Order {}'.format(order.id),
            'invoice': str(order.id),
            'currency_code': 'INR',
            'notify_url': 'http://{}{}'.format(host, reverse('paypal-ipn')),
            'return_url': 'http://{}{}'.format(host,reverse('payment:done')),
            'cancel_return': 'http://{}{}'.format(host, reverse('payment:canceled')),
            }
    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, 'payment/pdf.html', {'order': order,'form': form})'''
    html = render_to_string('payment/pdf.html', {'order': order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="order_{}.pdf"'.format(order.id)
    weasyprint.HTML(string=html).write_pdf(response,
                                           stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + 'css/pdf.css')])
    return response
    
def cod(request):
    order_id = request.session.get('order_id')
    
    return render(request, 'payment/pdf.html')
