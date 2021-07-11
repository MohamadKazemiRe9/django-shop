from django.shortcuts import render
from .forms import OrderCreateform
from .models import OrderItem
from cart.cart import Cart
from .tasks import order_created
# Create your views here.

def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateform(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,product=item['product'],price=item['price'],quantity=item['quantity'])
            cart.clear()
            order_created.delay(order.id)
            return render(request,'orders/order/created.html',{'order':order})
    else:
        form = OrderCreateform()
    return render(request,'orders/order/create.html',{"form":form,"cart":cart})