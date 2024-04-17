from django.shortcuts import render, redirect, get_object_or_404
from seller.models import Food
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Cart
# Create your views here.

def order_detail(request, pk):              #detail은 pk가 와줘야함.
    food = Food.objects.get(pk=pk)
    context = {
        'object': food
    }
    return render(request, 'order/order_detail.html', context=context)


@login_required
def cart_view(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.food.price * item.amount for item in cart_items)
    context = {
        'cart_items': cart_items,
        'total_price': total_price
    }
    return render(request, 'order/cart.html', context=context)

@login_required
def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        amount = int(request.POST.get('amount'))
        food = get_object_or_404(Food, pk=product_id)
        cart_item, created = Cart.objects.get_or_create(
            user=request.user,
            food=food,
            defaults={'amount': amount}
        )
        if not created:
            cart_item.amount += amount
            cart_item.save()
        return redirect('order:cart')
    return redirect('order:order_detail', pk=product_id)