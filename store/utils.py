import json
from .models import * 

def cookie_cart(request):
    # use a try block to prevent error if cookie doesn't exist
    try: 
        cart = json.loads(request.COOKIES['cart'])
    except: 
        cart = {}
    print('Cart:', cart)

    # create empty cart for non-logged in users
    items = []
    order = {'get_cart_total':0, 'get_cart_items':0}
    cartItems = order['get_cart_items']

    for i in cart: 
        # use a try block to prevent items in cart that may have been deleted from causing error
        try:
            cartItems += cart[i]['quantity']

            product = Product.objects.get(id=i)
            total = (product.price * cart[i]['quantity'])

            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]['quantity']

            item = {
                'product':{
                    'id':product.id,
                    'name': product.name, 
                    'price': product.price, 
                    'imageURL': product.imageURL
                }, 
                'quantity': cart[i]['quantity'],
                'get_total': total,
            }

            items.append(item)

            if product.digital == False: 
                order['shipping'] = True
        except: 
            pass
    return {'cartItems': cartItems, 'order': order, 'items': items}

def cart_data(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else: 
        cookie_data = cookie_cart(request)
        cartItems = cookie_data['cartItems']
        order = cookie_data['order']
        items = cookie_data['items']

    return {'cartItems': cartItems, 'order': order, 'items': items}

def guest_order(request, data):
    print('User is not logged in')

    print('COOKIES:', request.COOKIES)

    name = data['form']['name']
    email = data['form']['email']

    cookie_data = cookie_cart(request)
    items = cookie_data['items']

    # saves info of guest user so that we don't have to create new user
    # each time they check out
    customer, created = Customer.objects.get_or_create(
        email = email
    )
    customer.name = name
    customer.save()

    order = Order.objects.create(
        customer = customer, 
        complete = False, 
    )

    for item in items:
        product = Product.objects.get(id=item['product']['id'])
        order_item = OrderItem.objects.create(
            product = product, 
            order = order,
            quantity = item['quantity']
        )

    return customer, order