from django.urls import path

from . import views

urlpatterns = [
	#Leave as empty string for base url
    path('',views.logoutpage,name='logoutpage'),
	path('store/', views.store, name="store"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
    path('loginpage/', views.loginpage, name="loginpage"),
    path('logoutpage/', views.logoutpage, name="logoutpage"),


     path('registerpage/', views.registerpage, name="registerpage"),

    
	path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),

    


]