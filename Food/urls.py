from django.urls import path
from . import views
 
app_name = 'Food'

urlpatterns = [
    path('pizza', views.pizza, name='pizzas'),
    path('burgers', views.burger, name='burgers'),
    path('orders', views.order, name='order'),
    path('success', views.success, name='success'),
    path('signup', views.signup, name='signup'),
    path('login', views.logIn, name='login'),
    path('logout', views.logOut, name='logout'),
]