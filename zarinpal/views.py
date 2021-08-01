from django.shortcuts import render , get_object_or_404
from orders.models import Order
# Create your views here.
from django.http import HttpResponse
from django.shortcuts import redirect
from zeep import Client
from .config import MERCHANT
from .tasks import payment_completed

client = Client('https://www.zarinpal.com/pg/services/WebGate/wsdl')
amount = 1000  # Toman / Required
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
mobile = '09123456789'  # Optional
CallbackURL = 'http://localhost:8000/zarinpal/verify/' # Important: need to edit for realy server.

def send_request(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order,id=order_id)
    total_cost = order.get_total_cost()
    result = client.service.PaymentRequest(MERCHANT, total_cost, description, order.email, "mobile", CallbackURL)
    if result.Status == 100:
        return redirect('https://www.zarinpal.com/pg/StartPay/' + str(result.Authority))
    else:
        return HttpResponse('Error code: ' + str(result.Status))

def verify(request):
    if request.GET.get('Status') == 'OK':
        order_id = request.session.get('order_id')
        order = get_object_or_404(Order,id=order_id)
        result = client.service.PaymentVerification(MERCHANT, request.GET['Authority'], amount)
        if result.Status == 100:
            order.paid = True
            order.save()
            payment_completed.delay(order.id)
            # return HttpResponse('Transaction success.\nRefID: ' + str(result.RefID))
            return render(request,"zarinpal/success.html",{"id":result.RefID})
        elif result.Status == 101:
            # return HttpResponse('Transaction submitted : ' + str(result.Status))
            return render(request,"zarinpal/submited.html",{"status":result.Status})
        else:
            # return HttpResponse('Transaction failed.\nStatus: ' + str(result.Status))
            return render(request,"zarinpal/failed.html",{"status":result.Status})
    else:
        # return HttpResponse('Transaction failed or canceled by user')
        return render(request,"zarinpal/cancel.html",{})