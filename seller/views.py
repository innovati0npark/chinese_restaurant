from django.shortcuts import render, redirect
from .models import Food
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
# Create your views here.
# 판매자 페이지로 오면 자신이 판매중인 품목 리스트 보여주기. 
# 전체 Food에서 user(판매자)가 올린 food만 필터한다.
# Food.objects.all().filter(조건)
# 상품 등록하는 기능.

@login_required                 #로그인해야 접근가능.
def seller_index(request):
    foods = Food.objects.filter(user=request.user)
    context = {
        'object_list': foods
    }
    return render(request, 'seller/seller_index.html', context=context)
# request.user가 로그인 정보를 담고 있음.
# request.user
# <SimpleLazyObject: <User: innov>>
# <SimpleLazyObject: <django.contrib.auth.models.AnonymousUser object at 0x00000222408A5C90>> (로그인 안한경우)

def add_food(request):
    #get
    if request.method == "GET":
        return render(request, 'seller/seller_add_food.html')
    #post
    elif request.method =="POST":
        # foam에서 전달되는 값을 뽑아와서 DB에 저장.
        # food_name, price, description 가져왔었다. 
        # user_food = Food.objects.create(name=request.POST['user'])
        user = request.user
        food_name = request.POST['name']
        food_price = request.POST['price']
        food_description = request.POST['description']

        fs = FileSystemStorage()
        uploaded_file = request.FILES['file']
        name = fs.save(uploaded_file.name, uploaded_file)
        url = fs.url(name)
        Food.objects.create(user=user, name=food_name, price =food_price , description=food_description, image_url=url)        
        return redirect('seller:seller_index')

@login_required   
def food_detail(request, pk):
    food = Food.objects.get(pk=pk)
    context = {
        'object': food
    }
    return render(request, 'seller/seller_food_detail.html', context)

@login_required   
def food_delete(request, pk):
    object = Food.objects.get(pk=pk)
    object.delete()
    return redirect('seller:seller_index')