from django.shortcuts import render
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.forms import UserCreationForm 
from django.urls import reverse_lazy
from seller.models import Food

def index(request):
    foods = Food.objects.all()
    context = {
        'object_list': foods
    }
    return render(request, 'home.html', context=context)



class UserCreateView(CreateView): 
    template_name = 'registration/register.html' 
    form_class = UserCreationForm 
    success_url = reverse_lazy('register_done') 


class UserCreateDoneTV(TemplateView): 
    template_name = 'registration/register_done.html'