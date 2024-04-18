from django.shortcuts import render, redirect, get_object_or_404
from seller.models import Food
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Cart
from django.http import JsonResponse
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
        if not created:     #created 변수는 새로운 장바구니 항목이 생성되었는지 여부를 나타냄. 새로운 항목이 생성되지 않은 경우(이미 존재하는 경우), 기존 항목의 수량을 증가시킵니다.
            cart_item.amount += amount
            cart_item.save()
        return redirect('order:cart')
    return redirect('order:order_detail', pk=product_id) #POST 요청이 아닌 경우, 즉 사용자가 제품을 장바구니에 담는 것이 아닌 경우에 실행


# def modify_cart(request):
#     #어떤 사용자?
#     user = request.user
#     #어떤 음식?
#     product_id = request.POST.get('product_id')
#     #카트 정보 가져오기
#     cart, created = Cart.objects.get(food__id=product_id, user=user)
#     #수량 업데이트
#     cart.amount += int(request.POST['amountChange'])
#     if cart.amount > 0:
#         cart.save()
#     #Json
#     context = {
#         'newQuantity' : cart.amount,
#         'totalQuantity' : cart.amount,
#         'message':'성공!',
#         'success': True
#     }
#     return JsonResponse

def modify_cart(request, cart_item_id):
    if request.method == 'POST':
        quantity = int(request.GET.get('quantity'))
        cart_item = Cart.objects.filter(id=cart_item_id)
        cart_item.amount += quantity
        cart_item.save()

        cart = Cart.objects.get(user=request.user)
        cart_items = Cart.objects.filter(cart=cart)
        total_price = sum(item.food.price * item.amount for item in cart_items)

        return JsonResponse({
            'amount': cart_item.amount,
            'total_price': cart_item.food.price * cart_item.amount,
            'cart_total_price': total_price
        })
    return JsonResponse({'error': 'Invalid request method'}, status=400)


def update_cart(request, cart_item_id):
    cart_item = get_object_or_404(Cart, id=cart_item_id)
    new_amount = int(request.POST['amount'])
    cart_item.amount = new_amount
    cart_item.save()
    return redirect('cart')