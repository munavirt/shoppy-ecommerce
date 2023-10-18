from django.shortcuts import render,redirect
from django.contrib import messages
from store.models import Product, Banner
from datetime import datetime
from accounts.models import Account
from django.contrib.auth import authenticate, login
import requests
from .models import ContactUs
# Create your views here.

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

# Verification email




def home(request):
    products = Product.objects.all().filter(is_available=True)
    banners = Banner.objects.all().filter(is_available=True)
    la_products = Product.objects.order_by('-created_date')[:4]
    up_products = Product.objects.filter(created_date__gte=datetime.now(), is_available=True)[:4]
    context = {
        'products':products,
        'banners' : banners,
        'la_products' : la_products,
        'up_products' : up_products,
    }
    return render(request,'index.html',context)


def blog(request):
    return render(request,'index.html')

def cp_register(request):
    if request.method == 'POST':
        first_name = request.POST.get('fname')
        last_name = request.POST.get('lname')
        email = request.POST.get('email')
        phone_number = request.POST.get('mobile')
        password = request.POST.get('password')
        re_password = request.POST.get('rePassword')

        # perform validation on the input data
        if password != re_password:
            # handle password mismatch error
            pass
        elif Account.objects.filter(email=email).exists():
            # handle email already exists error
            pass
        elif Account.objects.filter(phone_number=phone_number).exists():
            # handle phone number already exists error
            pass
        else:
            # create a new account and save it to the database
            user = Account.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                username=email,  # use email as the default username
                password=password,
                phone_number=phone_number
            )
            
            current_site = get_current_site(request)
            mail_subject = 'please activate your account'
            message = render_to_string('account_verify_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            # redirect the user to a success page
            return redirect('cp_login/?command=verification$email='+ email)
        
    return render(request,'register2.html')

def cp_activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulations! Your account is activated.')
        return redirect('cp_login')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('cp_register')


def cp_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home') # Replace 'home' with the name of your homepage URL pattern
        else:
            error_message = 'Invalid login credentials'
    else:
        error_message = ''

    return render(request,'login2.html')


def single_blog(request):
    return render(request,'order_complete.html')


def checkout(request):
    return render(request,'payments.html')


def confirmation(request):
    return render(request,'confirmation.html')


def contact_us(request):
    if request.method == 'POST':
        name=request.POST['name']
        email=request.POST['email']
        message=request.POST['subject']
        
        usermessage = ContactUs.objects.create(name=name,email=email,message=message)
        
        usermessage.save()
        messages.success(request,'Thank you for contacting Fresh Harvest, We will reply your message soon!')
        
    return render(request,'contact.html')


def elements(request):
    return render(request,'elements.html')


def tracking(request):
    return render(request,'tracking.html')


def api_call(request):
    # api_url = 'https://api.storerestapi.com/products/running-sneaker'
    # response = requests.get(api_url)
    # if response.status_code == 200:
    #     data = response.json()
    #     context = {'data': data}
    #     return render(request, 'api.html', context)
    # else:
    #     error_message = f"Error {response.status_code} occurred."
    
    response = requests.get('https://api.storerestapi.com/products/running-sneaker')
    data = response.json()
    return render(request, 'api.html',{'product': data})


