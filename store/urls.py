from django.urls import path
from . import views


urlpatterns = [
    path('', views.store, name='home'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name="checkout"),
    path('registration/', views.register, name='registration'),
    path('login/', views.loginpage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('update_item/', views.update_cart),
    path('place_order/', views.placeOrder),
    path('myorders/',views.myOrder),
    path('update_myorders/',views.update_myorder),
    path('product/<int:id>/' ,views.view),

]
