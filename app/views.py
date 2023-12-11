from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import Product, Customer, Cart, Orderplaced
from django.views import View
from .forms import CustomerRegistrationForm, CustomerProfileForm, EmailMessageForm
from django.contrib import messages
from django.core.mail import EmailMessage, get_connection
from django.conf import settings

# Create your views here.


class HomeView(View):
    def get(self, request):
        fiction = Product.objects.filter(category="F")
        mystery = Product.objects.filter(category="M")
        romance = Product.objects.filter(category="R")
        return render(request, 'app/home.html', {'fiction': fiction, 'mystery': mystery, 'romance': romance})


class ProductDetail(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        item_already_in_cart = False
        if request.user.is_authenticated:
            item_already_in_cart = Cart.objects.filter(Q(user=request.user) & Q(product=product.id)).exists()
        return render(request, 'app/productdetail.html', {'product': product, 'item_already_in_cart': item_already_in_cart})


def fiction(reqeust, data=None):
    if data == None:
        fict = Product.objects.all()
    if data == "Fiction":
        fict = Product.objects.filter(category='F')
    elif data == "Romance":
        fict = Product.objects.filter(category='R')
    elif data == "Mystery":
        fict = Product.objects.filter(category='M')
    elif data == "Horror":
        fict = Product.objects.filter(category='H')
    return render(reqeust, 'app/fiction.html', {'fiction': fict})


class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', {'form':form})
    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Congratulations! You've successfully created an account.")
        return render(request, 'app/customerregistration.html', {'form': form})


class Profile(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary'})
    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            zipcode = form.cleaned_data['zipcode']
            state = form.cleaned_data['state']
            reg = Customer(user=usr, name=name, locality=locality, city=city, zipcode=zipcode, state=state)
            reg.save()
            messages.success(request, "Congratulations!! Your profile Successfully Update")
        return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary'})


def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html', {'add': add, 'active': 'btn-primary'})


def add_to_cart(request):
    if request.user.is_authenticated:
        user = request.user
        product_id = request.GET.get('prod_id')
        product = Product.objects.get(id=product_id)
        Cart(user=user, product=product).save()
        return redirect('/cart')
    else:
        return redirect('login')


def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0.0
        shipping_charge = 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]

        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount += tempamount
                total_amount = amount + shipping_charge
            return render(request, 'app/addtocart.html', {'carts': cart, 'amount': amount, 'total_amount': total_amount})
        else:
            return render(request, 'app/emptycart.html')


def plus_cart(request):
    if request.method == "GET":
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
            total_amount = amount + shipping_amount

        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': total_amount
        }

        return JsonResponse(data)


def minus_cart(request):
    if request.method == "GET":
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity -= 1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
            total_amount = amount + shipping_amount

        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': total_amount
        }

        return JsonResponse(data)


def remove_cart(request):
    if request.method == "GET":
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
            total_amount = amount + shipping_amount

        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': total_amount
        }

        return JsonResponse(data)


def checkout(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 70.0
    total_amount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    if cart_product:
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
        total_amount = amount + shipping_amount

    return render(request, 'app/checkout.html', {'add': add, 'totalamount': total_amount, 'cart_items': cart_items})


def payment(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        Orderplaced(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
        c.delete()
    return redirect('orders')


def order(request):
    op = Orderplaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html', {'order_placed': op})


def delete_item(request, id):
    if request.method == "POST":
        pi = Product.objects.get(pk=id)
        pi.delete()
        return redirect('orders')


class send_email(View):
    def get(self, request):
        return render(request, 'app/contact.html')

    def post(self, request):
        if request.method == 'POST':
            with get_connection(host=settings.EMAIL_HOST, port=settings.EMAIL_PORT, username=settings.EMAIL_HOST_USER, password=settings.EMAIL_HOST_PASSWORD, use_tls=settings.EMAIL_USE_TLS) as connection:
                subject = request.POST.get('subject')
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [request.POST.get('email')]
                message = request.POST.get('message')
                EmailMessage(subject, message, email_from, recipient_list, connection=connection).send()
            return render(request, 'app/contact.html')
        return redirect('/')