from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
from delivery.models import Customer,Restaurant,MenuItem,Cart
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request,'delivery/index.html')

def signin(request):
    return render(request,'delivery/signin.html')

def signup(request):
    return render(request,'delivery/signup.html')

def handle_login(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')

        try:
            Customer.objects.get(username=username,password=password)
            if username == 'admin':
                return render(request,'delivery/success.html')
            else:
                restaurants = Restaurant.objects.all()
                return render(request,'delivery/customer_home.html',{"restaurants":restaurants,"username":username})
        except Customer.DoesNotExist:
            return render(request,'delivery/fail.html')
    else:
        return HttpResponse("Invalid request")

def handle_signup(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        email=request.POST.get('email')
        mobile=request.POST.get('mobile')
        address=request.POST.get('address')

        try:
            cust=Customer.objects.get(username=username)
        except:
            c=Customer(username=username,password=password,email=email,mobile=mobile,address=address)
            c.save()

        return render(request,'delivery/signin.html')
        #return HttpResponse(f"username : {username},password : {password},Email : {email},Mobile : {mobile},Address : {address}")
    else:
        return HttpResponse("Invalid request")
    
def restaurant_page(request):
    return render(request,'delivery/add_restaurant.html')

def add_restaurant(request):
    if request.method=='POST':
        name=request.POST.get('name')
        picture=request.POST.get('picture')
        cuisine=request.POST.get('cuisine')
        rating=request.POST.get('rating')

        rest=Restaurant(name=name,picture=picture,cuisine=cuisine,rating=rating)
        rest.save()

        restaurants=Restaurant.objects.all()

        return render(request,'delivery/show_restaurants.html',{"restaurants":restaurants})
    else:
        return HttpResponse("invalid request")
    
def show_restaurant_page(request):
    restaurants=Restaurant.objects.all()
    return render(request,'delivery/show_restaurants.html',{"restaurants":restaurants})

def restaurant_menu(request,restaurant_id):
    restaurant=get_object_or_404(Restaurant,id=restaurant_id)
    if request.method=='POST':
        name=request.POST.get('name')
        description=request.POST.get('description')
        price=request.POST.get('price')
        is_veg=request.POST.get('is_veg')=='on'
        picture=request.POST.get('picture')

        MenuItem.objects.create(
            restaurant=restaurant,
            name=name,
            description=description,
            price=price,
            is_veg=is_veg,
            picture=picture
        )
        return redirect('restaurant_menu',restaurant_id=restaurant.id)
    menu_items=restaurant.menu_items.all()
    return render(request,'delivery/menu.html',{
        'restaurant':restaurant,
        'menu_items':menu_items,
    })

def update_restaurant_page(request,restaurant_id):
    restaurant=get_object_or_404(Restaurant,id=restaurant_id)
    return render(request,'delivery/update_restaurant_page.html',{"restaurant":restaurant})

def update_restaurant(request,restaurant_id):
    restaurant=get_object_or_404(Restaurant,id=restaurant_id)
    if request.method=='POST':
        restaurant.name=request.POST.get('name')
        restaurant.picture=request.POST.get('picture')
        restaurant.cuisine=request.POST.get('cuisine')
        restaurant.rating=request.POST.get('rating')
        restaurant.save()
        restaurants=Restaurant.objects.all()
        return render(request,'delivery/show_restaurants.html',{"restaurants":restaurants})
    
def delete_restaurant(request,restaurant_id):
    restaurant=get_object_or_404(Restaurant,id=restaurant_id)
    restaurant.delete()
    restaurants=Restaurant.objects.all()
    return render(request,'delivery/show_restaurants.html',{"restaurants":restaurants})

def update_menuItem_page(request,menuItem_id):
    menuItem=get_object_or_404(MenuItem,id=menuItem_id)
    return render(request,'delivery/update_menuItem_page.html',{"menuItem":menuItem})

def update_menuItem(request,menuItem_id):
    menuItem=get_object_or_404(MenuItem,id=menuItem_id)
    if request.method=='POST':
        menuItem.name=request.POST.get('name')
        menuItem.description=request.POST.get('description')
        menuItem.price=request.POST.get('price')
        menuItem.is_veg=request.POST.get('is_veg')=='on'
        menuItem.picture=request.POST.get('picture')
        menuItem.save()
        restaurants=Restaurant.objects.all()
        return render(request,'delivery/show_restaurants.html',{"restaurants":restaurants})
    
def delete_menuItem(request,menuItem_id):
    menuItem=get_object_or_404(MenuItem,id=menuItem_id)
    menuItem.delete()
    restaurants=Restaurant.objects.all()
    return render(request,'delivery/show_restaurants.html',{"restaurants":restaurants})

def customer_menu(request,restaurant_id,username):
    restaurant=get_object_or_404(Restaurant,id=restaurant_id)
    menu_items=restaurant.menu_items.all()
    return render(request,'delivery/customer_menu.html',{
        'restaurant':restaurant,
        'menu_items':menu_items,
        'username':username
    })

def show_cart_page(request, username):
    customer = get_object_or_404(Customer, username=username)
    cart = Cart.objects.filter(customer=customer).first()

    items = cart.items.all() if cart else []
    total_price = cart.total_price() if cart else 0

    return render(request, 'delivery/cart.html', {
        'items': items,
        'total_price': total_price,
        'username': username,
    })

def add_to_cart(request, item_id, username):
    customer = get_object_or_404(Customer, username=username)
    item = get_object_or_404(MenuItem, id=item_id)
    cart, created = Cart.objects.get_or_create(customer=customer)
    cart.items.add(item)
    messages.success(request,f"{item.name} added to your cart!")
    return redirect('customer_menu',restaurant_id=item.restaurant.id,username=username)

def checkout(request, username):
    customer = get_object_or_404(Customer, username=username)
    cart = Cart.objects.filter(customer=customer).first()

    cart_items = cart.items.all() if cart else []
    total_price = cart.total_price() if cart else 0

    if total_price == 0:
        return render(request, 'delivery/checkout.html', {
            'error': 'your cart is empty!',
            'username': username
        })

    return render(request, 'delivery/checkout.html', {
        'username': username,
        'cart_items': cart_items,
        'total_price': total_price,
    })
    
def orders(request, username):
    customer = get_object_or_404(Customer, username=username)
    cart = Cart.objects.filter(customer=customer).first()

    cart_items = list(cart.items.all()) if cart else []
    total_price = cart.total_price() if cart else 0

    if cart:
        cart.items.clear()

    return render(request, 'delivery/orders.html', {
        'username': username,
        'customer': customer,
        'cart_items': cart_items,
        'total_price': total_price,
        'address': customer.address,
    })

def remove_from_cart(request, item_id, username):
    customer = get_object_or_404(Customer, username=username)
    cart = Cart.objects.filter(customer=customer).first()

    if cart:
        item = get_object_or_404(MenuItem, id=item_id)
        cart.items.remove(item)

    return redirect('show_cart_page', username=username)
