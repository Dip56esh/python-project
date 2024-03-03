from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime
from .models import *

# Create your views here.

def store(request):

	if request.user.is_authenticated:
		customer=request.user.customer
		order, created = Order.objects.get_or_create(customer=customer,complete=False)
		items=order.orderitem_set.all()
		cartItems=order.get_cart_item
	else:
		items=[]
		order={'get_cart_total':0,'get_cart_item':0,'shipping':False}
		cartItems=order['get_cart_item']

	products=Product.objects.all()
	context = {'products':products,'cartItems':cartItems}
	return render(request, 'store/store.html', context)

def cart(request):
	if request.user.is_authenticated:
		customer=request.user.customer
		order, created = Order.objects.get_or_create(customer=customer,complete=False)
		items=order.orderitem_set.all()
		cartItems=order.get_cart_item

	else:
		items=[]
		order={'get_cart_total':0,'get_cart_item':0,'shipping':False}
		cartItems=order['get_cart_item']


	context = {'items':items,'order':order,'cartItems':cartItems}
	return render(request, 'store/cart.html', context)

def checkout(request):

	if request.user.is_authenticated:
		customer=request.user.customer
		order, created = Order.objects.get_or_create(customer=customer,complete=False)
		items=order.orderitem_set.all()
		cartItems=order.get_cart_item

	else:
		items=[]
		order={'get_cart_total':0,'get_cart_item':0,'shipping':False}
		cartItems=order['get_cart_item']



	context = {'items':items,'order':order,'cartItems':cartItems}
	return render(request, 'store/checkout.html', context)


def updateItem(request):
	data=json.loads(request.body)
	product_id=data['productId']
	action=data['action']
	print("productId",product_id)
	print('Action', action)


	customer=request.user.customer
	product=Product.objects.get(id=product_id)
	order,created=Order.objects.get_or_create(customer=customer,complete=False)

	orderItem,created=OrderItem.objects.get_or_create(Order=order, Product=product)
	if  action=="add":
		orderItem.quantity=orderItem.quantity+1
	elif action=='remove':
		orderItem.quantity=orderItem.quantity-1
	orderItem.save()

	if orderItem.quantity<=0:
		orderItem.delete()

	return JsonResponse('item was added',safe=False)

def processOrder(request):
	transcation_id=datetime.datetime.now().timestamp()
	data=json.loads(request.body)
	if(request.user.is_authenticated):
		customer=request.user.customer
		order,created=Order.objects.get_or_create(customer=customer,complete=False)
		total=float(data['form']['total'])
		order.transaction_id=transcation_id

		if total==order.get_cart_total:
			order.complete=True
		order.save()

		if order.shipping==True:
			ShippingAddress.objects.create(
				customer=customer,
				Order=order,
				address=data['shipping']['address'],
				city=data['shipping']['city'],
				state=data['shipping']['state'],
				zipcode=data['shipping']['zipcode'],
			)

	else:
		print('user is not logged in..')
	return JsonResponse('Payment Completed',safe=False)

def login(request):
	return render(request, 'store/login.html')

def processLogin(request):
	pass