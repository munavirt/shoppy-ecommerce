from django.shortcuts import render, redirect
from accounts.models import *
from store.models import *
from category.models import *
from orders.models import *
from django.http import HttpResponse
import calendar
from datetime import datetime,timedelta
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from django.contrib.auth import authenticate, login
from django.contrib import messages, auth
from django.core.paginator import Paginator
from .forms import productForm

from core.models import ContactUs
from django.core.mail import EmailMessage


from django.db.models import Sum



def admin_login(request):
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = auth.authenticate(request, username=username, password=password)
        

        if user is not None and user.is_active and user.is_superadmin:
            login(request, user)
            
            return redirect('admin_dasboard')
        
        else:
            return render(request, 'admin_login.html', {'error_message' : 'Invalid Credentials'})
        
    else:
        return render(request, 'admin_login.html')
    
    
def admin_logout(request):
    auth.logout(request)
    messages.success(request, 'Your are Logged out')
    return redirect('admin_login')



def dashboard(request):
    total_users = Account.objects.count()
    total_product = Product.objects.count()
    total_categorey = Category.objects.count()
    total_orders = OrderProduct.objects.count()
    total_coupon = Coupon.objects.count()
    total_sales = OrderProduct.objects.filter(ordered=True).aggregate(Sum('product_price'))['product_price__sum']
    
    today = datetime.today()
    this_year = today.year
    this_month = today.month
    
    # Define first_order_date
    # first_order_date = Order.objects.earliest('created_at').created_at
    
    # label_list = []
    # line_data_list = []
    # bar_data_list =  []
    # month_list=[]
    # for year in range(first_order_date.year,this_year+1) :
    #     month = this_month if year==this_year else 12
    #     month_list= month_list+(list(map(lambda x : calendar.month_abbr[x]+'-'+str(year),range(1,month+1))))[::-1]
    # for year in range(2022,(this_year+1)):
    #     this_month = this_month if year==this_year else 12
    #     for month in range(1,(this_month+1)):
    #         month_wise_total_orders = Order.objects.filter(is_ordered=True,created_at__year = year,created_at__month=month,).order_by('created_at').count()
    #         month_name = calendar.month_abbr[month]
    #         label_update = str(month_name)+ ' ' + str(year)
    #         label_list.append(label_update)
    #         line_data_list.append(month_wise_total_orders)
    # for year in range(2022,(this_year+1)):
    #     for month in range(1,(this_month+1)):
    #         monthwise_orders = Order.objects.filter(is_ordered=True,created_at__year = year,created_at__month=month,)
    #         monthwise_sales  = round(sum(list(map(lambda x : x.order_total,monthwise_orders))),2)
    #         bar_data_list.append(monthwise_sales)
    context = {
        'total_users' :total_users,
        'total_product' : total_product,
        'total_categorey' : total_categorey,
        'total_orders' : total_orders,
        'total_coupon' : total_coupon,
        'total_sales' : total_sales,
        # 'month_list'      : month_list,
        # 'line_labels'     : label_list,
        # 'line_data'       : line_data_list,
        # 'bar_data'        : bar_data_list
    }
    return render(request,'admindashboard.html', context)


# @login_required(login_url='admin_login')
def admin_product(request):
    products = Product.objects.all().filter(is_available=True)
    category = Category.objects.all()

    context = {
        'products' : products,
        'category' : category
    }
    
    return render(request,'admin_product.html',context)


def admin_addProduct(request):
    if request.method == 'POST':
        # Extract form data from the POST request
        product_name = request.POST.get('product_name')
        slug = request.POST.get('slug')
        description = request.POST.get('description')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        is_available = request.POST.get('is_available')
        is_featured = request.POST.get('is_featured')
        category_id = request.POST.get('category')  # Assuming category is sent as ID
        
        # Handle image upload
        image = request.FILES.get('images')  # Assuming the input name is 'images'
        
        # Save the form data into the Product model
        product = Product(
            product_name=product_name,
            slug=slug,
            description=description,
            price=price,
            stock=stock,
            is_available=bool(is_available),
            is_featured=bool(is_featured),
            category_id=category_id,  # Assuming category is sent as ID
            images=image  # Save the image
        )
        product.save()

        return HttpResponse('Product successfully added!')  # Modify this as needed

    # Fetch categories to populate the dropdown in the form
    categories = Category.objects.all()
    
    return render(request, 'admin_addProduct.html', {'categories': categories})


def adminCategory(request):
    brand = Category.objects.all()
    context = {
        brand : "brand"
    }

    return render(request,'admin_category.html',context)




# @login_required(login_url = 'admin_login')
def adminMessages(request):
    messages_recieved  = ContactUs.objects.all().order_by('-sent_time')
    context = {
        'messages_recieved' : messages_recieved,
    }
    return render(request,'admin_messages.html',context)


# @login_required(login_url = 'admin_login')
def deleteMessage(request,id):
    message = ContactMessage.objects.get(id=id)
    message.delete()
    messages.error(request,'message deleted successfully!')
    return redirect('adminMessages')


# @login_required(login_url = 'admin_login')
def replyMessage(request):
    try:
        if request.method == 'POST':
            email = request.POST['email']
            message = request.POST['message']
            mail_subject = ''' Reply from Fresh Harvest Ecommerce shop'''
            send_mail = ContactUs(mail_subject,message,to=[email])
            send_mail.send()
            messages.success(request,'Message sent successfully')
            return redirect('adminMessages')
        else:
            messages.error(request,'please fill the form correctly')
        
    except:
        messages.error(request,'Server down! please ensure you are connected to internet')
        return redirect('adminMessages')
        