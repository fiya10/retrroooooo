from django.conf import settings
import json
from django.shortcuts import render
from .cart import Cart

def cart_detail(request):
    cart = Cart(request)
    products = []

    for item in cart:
        product = item['product']
        product_details = {
            'id': product.id,
            'title': product.title,
            'price': str(product.price),
            'quantity': int(item['quantity']),
            'total_price': str(item['total_price']),
            'url': f'/{product.category.slug}/{product.slug}/',
            'num_available': product.num_available
        }
        products.append(product_details)

    products_json = json.dumps(products)

    if request.user.is_authenticated:
        user_data = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
        }
    else:
        user_data = {'first_name': '', 'last_name': '', 'email': ''}

    context = {
        'cart': cart,
        'pub_key': settings.STRIPE_API_KEY_PUBLISHABLE,
        'products_json': products_json,
        **user_data
    }
    return render(request, 'cart.html', context)

def success(request):
    cart = Cart(request)
    cart.clear()
    return render(request, 'success.html')
