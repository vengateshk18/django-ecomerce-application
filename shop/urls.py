from django.urls import path
from . import views

urlpatterns = [
    path('home',views.home,name='home'),
    path('register',views.register,name="register"),
    path('',views.home,name="home"),
    path('logout',views.logout_page,name="logout"),
    path('login',views.login_page,name="login"),
    path('collections',views.collections,name="collections"),
    path('collections/<str:category>',views.collections_product,name="collections_product"),
    path('collections/<str:cname>/<str:pname>',views.product_name,name="product_name"),
    path('addtocart',views.add_cart,name="addtocart"),
    path('Cart',views.cart,name="cart"),
    path('RemoveCart/<str:pid>',views.removeCart,name="RemoveCart")
    ]