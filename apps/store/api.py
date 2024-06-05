import json
import stripe
from django.http import JsonResponse
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect
from apps.cart.cart import Cart
from .models import Product
from apps.order.utils import checkout
from apps.order.models import Order, OrderItem

def create_checkout_session(request):
    cart = Cart(request)
    stripe.api_key = settings.STRIPE_API_KEY_HIDDEN
    items = []
    total_price = 0  # Initialize total_price

    for item in cart:
        product = item['product']
        price = int(float(product.price) * 100)  # Stripe expects amount in cents
        total_price += (price * int(item['quantity']))

        obj = {
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': product.title
                },
                'unit_amount': price
            },
            'quantity': item['quantity']
        }

        items.append(obj)

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=items,
        mode='payment',
        success_url='http://127.0.0.1:8000/cart/success/',
        cancel_url='http://127.0.0.1:8000/cart/'
    )

    #create order
    data = json.loads(request.body)
    first_name = data['first_name']
    last_name = data['last_name']
    email = data['email']
    address = data['address']
    zipcode = data['zipcode']
    place = data['place']
    payment_intent = session.payment_intent

    orderid = checkout(request, data['first_name'], data['last_name'], data['email'], data['address'], data['zipcode'], data['place'], data['phone'])
    order = Order.objects.get(pk=orderid)
    order.payment_intent = payment_intent
    order.paid_amount = cart.get_total_cost()
    order.save()

    return JsonResponse({'session': session})

def api_checkout(request):
    cart = Cart(request)
    data = json.loads(request.body)
    jsonresponse = {'success': True}
    
    first_name = data['first_name']
    last_name = data['last_name']
    email = data['email']
    address = data['address']
    zipcode = data['zipcode']
    place = data['place']

  
    paid = True

    if paid:
        order = Order.objects.get(pk=orderid)
        order.paid = True
        order.paid_amount = cart.get_total_cost()
        order.save()

        cart.clear()
        return JsonResponse(jsonresponse)
    
    if cart.get_total_cost() > 0:
        order = Order.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            address=address,
            zipcode=zipcode,
            place=place,
            paid_amount=cart.get_total_cost(),
        )

        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                price=item['price'],
                quantity=item['quantity']
            )

        cart.clear()
        jsonresponse['order_id'] = order.id
    else:
        jsonresponse = {'success': False, 'error': 'Cart is empty'}
    
    return JsonResponse(jsonresponse)

def api_add_to_cart(request):
    cart = Cart(request)
    try:
        data = json.loads(request.body)
        product_id = data.get('product_id')
        quantity = data.get('quantity', 1)
        update = data.get('update', False)
        
        product = Product.objects.get(id=product_id)
        
        cart.add(product=product, quantity=quantity, update_quantity=update)
        
        return JsonResponse({'success': True})
    except Product.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Product does not exist'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
    
def api_increment_quantity(request):
    cart = Cart(request)
    try:
        data = json.loads(request.body)
        product_id = str(data['product_id'])
        
        cart.increment(product_id)
        
        return JsonResponse({'success': True})
    except Product.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Product does not exist'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

def api_remove_from_cart(request):
    cart = Cart(request)
    try:
        data = json.loads(request.body)
        product_id = str(data['product_id'])

        cart.remove(product_id)

        return JsonResponse({'success': True})
    except Product.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Product does not exist'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
