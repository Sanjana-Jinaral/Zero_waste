from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.index),
    path('signin/',views.signin),
    path('signup/',views.signup),
    path('handle_login/',views.handle_login,name='handle_login'),
    path('handle_signup/',views.handle_signup,name='handle_signup'),
    path('handle_login/restaurant_page/',views.restaurant_page,name='restaurant_page'),
    path('handle_login/add_restaurant/',views.add_restaurant,name='add_restaurant'),
    path('restaurant/<int:restaurant_id>/menu/',views.restaurant_menu,name='restaurant_menu'),
    path('handle_login/show_restaurant_page/',views.show_restaurant_page,name='show_restaurant_page'),
    path('restaurants/<int:restaurant_id>/update/',views.update_restaurant,name='update_restaurant'),
    path('restaurants/<int:restaurant_id>/update/page/',views.update_restaurant_page,name='update_restaurant_page'),
    path('restaurants/<int:restaurant_id>/delete/',views.delete_restaurant,name='delete_restaurant'),
    path('menu/<int:menuItem_id>/update/',views.update_menuItem,name='update_menuItem'),
    path('menu/<int:menuItem_id>/update/page/',views.update_menuItem_page,name='update_menuItem_page'),
    path('menu/<int:menuItem_id>/delete/',views.delete_menuItem,name='delete_menuItem'),
    path('restaurants/<int:restaurant_id>/menu/customer/<str:username>',views.customer_menu,name='customer_menu'),
    path('cart/<str:username>/', views.show_cart_page, name='show_cart_page'),
    path('cart/<int:item_id>/add/<str:username>/',views.add_to_cart,name='add_to_cart'),
    path('checkout/<str:username>/',views.checkout,name='checkout'),
    path('orders/<str:username>/',views.orders,name='orders'),
    path('cart/<int:item_id>/remove/<str:username>/', views.remove_from_cart, name='remove_from_cart'),
]