from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from votings.models import Product
from .cart import Cart
from .forms import CartAddProductForm


@require_POST
def cart_add(request, product_id):
    print("I am in add to cart")
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'], update_quantity=cd['update'])
    return redirect('cart:cart_detail')


def cart_remove(request, product_id):
    print("I am in remove cart")
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    print("I am rendering cart, inside cart_detail")
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'], 'update': True})
    room=request.session.get('currentRoom') 
    user=request.session.get('customer_name')
    print(room)
    return render(request, 'cart/detail.html', {'cart': cart,'room':room,'user':user})

