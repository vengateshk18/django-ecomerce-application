import json
from django.http import JsonResponse
from django.shortcuts import *
from . models import *
from .models import Cart
from shop.forms import CustomUserForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
import json
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from .models import Products, Cart 
def home(request):
    category=Catagory.objects.filter(status=0)
    products=Products.objects.filter(trending=1)
    return render(request,'home.html',{"product":products,"category":category})

def removeCart(request,pid):
   cartitem=Cart.objects.get(id=pid)
   cartitem.delete()
   return redirect('/Cart') 

 
def add_cart(request):
   if request.headers.get('x-requested-with')=='XMLHttpRequest':
    if request.user.is_authenticated:
      data=json.load(request)
      product_qty=data['product_qty']
      product_id=data['pid']
      #print(request.user.id)
      product_status=Products.objects.get(id=product_id)
      if product_status:
        if Cart.objects.filter(user=request.user.id,product_id=product_id):
          return JsonResponse({'status':'Product Already in Cart'}, status=200)
        else:
          if product_status.quantity>=product_qty:
            Cart.objects.create(user=request.user,product_id=product_id,product_qty=product_qty)
            return JsonResponse({'status':'Product Added to Cart'}, status=200)
          else:
            return JsonResponse({'status':'Product Stock Not Available'}, status=200)
    else:
      return JsonResponse({'status':'Login to Add Cart'}, status=200)
   else:
    return JsonResponse({'status':'Invalid Access'}, status=200)
def cart(request):
   if request.user.is_authenticated:
      cart=Cart.objects.filter(user=request.user)
      return render(request,'cart.html',{"product":cart})
   else:
      return redirect('home')
def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,"Logged out successfully")
        return redirect("/")
def login_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    elif request.method=='POST':
        name=request.POST.get('username')
        pwd=request.POST.get('password')
        user=authenticate(request,username=name,password=pwd)
        if user is not None:
            login(request,user)
            messages.success(request, f"Logged in successfully!!! {user}")
            return redirect('home')
        else:
            messages.error(request,"Invalid Username Or Password")
            return redirect('login')
    return render(request,'login.html')
def register(request):
    form=CustomUserForm()
    if request.method=='POST':
        form=CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Registration success and you can login now")
            return redirect('/login')
    return render(request,'register.html',{"form":form})
def collections(request):
    catagory=Catagory.objects.filter(status=0)
    return render(request,'collections.html',{"catagory":catagory})
def collections_product(request,category):
   if(Catagory.objects.filter(name=category,status=0)):
       products=Products.objects.filter(category__name=category)
       return render(request,'products/product.html',{"products":products,"category":category})
   else:
       messages.warning(request,"this is not a valid url")
       return redirect('collections')
def product_name(request,cname,pname):
    if(Catagory.objects.filter(name=cname,status=0)):
        if(Products.objects.filter(name=pname,status=0)):
            product=Products.objects.filter(name=pname,status=0).first()
            return render(request,'products/product_details.html',{"product":product,"category":cname})
        else:
            messages.warning("product not available")
            return redirect('collections')
    else:
        messages.warning("category not found")
        return redirect('collection')