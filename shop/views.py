from django.shortcuts import render , get_object_or_404
from .models import Category , Product
from cart.forms import CartAddProductForm

# Create your views here.

def product_list(request,category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category,slug=category_slug)
        products = products.filter(category=category)
    context = {
            'categories':categories,
            "category":category,
            "products":products
    }
    return render(request,'shop/product/list.html',context)

def product_detail(request,id,slug):
    product = get_object_or_404(Product,id=id,slug=slug,available=True)
    cart_product_form = CartAddProductForm()
    context = {
        'product':product,
        'form':cart_product_form,
    }
    return render(request, "shop/product/detail.html",context)

