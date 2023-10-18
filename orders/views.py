

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest
from carts.models import CartItem
from .forms import OrderForm
from django.contrib import messages, auth
from .models import Order, Payment
from accounts.models import Account
from store.models import Product
import datetime
import json
from django.http import JsonResponse
from .models import Order, Payment, OrderProduct
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt # new
from django.views.generic.base import TemplateView
from django.views import View
from django.core.mail import EmailMessage
from django.core.mail import EmailMessage
from django.template.loader import render_to_string, get_template
# from weasyprint import HTML
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch

from twilio.rest import Client

import io
import requests
from django.templatetags.static import static



# Create your views here.
# def coupon(request):
#   if request.method == 'POST':
#     coupon_code = request.POST['coupon']
#     grand_total = request.POST['grand_total']
#     coupon_discount = 0
#     try:
#       instance = UserCoupon.objects.get(user = request.user ,coupon__code = coupon_code)

#       if float(grand_total) >= float(instance.coupon.min_value):
#         coupon_discount = ((float(grand_total) * float(instance.coupon.discount))/100)
#         grand_total = float(grand_total) - coupon_discount
#         grand_total = format(grand_total, '.2f')
#         coupon_discount = format(coupon_discount, '.2f')
#         msg = 'Coupon Applied successfully'
#         instance.used = True
#         instance.save()
#       else:
#           msg='This coupon is only applicable for orders more than ₹'+ str(instance.coupon.min_value)+ '\- only!'
#     except:
#             msg = 'Coupon is not valid'
#     response = {
#                'grand_total': grand_total,
#                'msg':msg,
#                'coupon_discount':coupon_discount,
#                'coupon_code':coupon_code,
#                 }

#   return JsonResponse(response)


def place_order(request, total=0, quantity=0,):
    current_user = request.user
    
    # if the cart count is less than or equal to 0, then redirect back to shop
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    
    if cart_count <= 0:
        return redirect('category')
    
    grand_total = 0
    
    
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # store all the billing information inside order table
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            
            # generate order number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d") #20210305
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()
            
            
            order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
            
            context = {
                'order' : order,
                'cart_items' : cart_items,
                'total': total,
                'grand_total' : grand_total
                
            }
            
            return render(request,'payments.html',context)
        else:
            return redirect('checkout')
    else:
        return redirect('checkout')
    
    


def payments(request):
    body = json.loads(request.body)
    order = Order.objects.get(user=request.user, is_ordered=False, order_number=body['orderID'])
    payment = Payment(
        user = request.user,
        payment_id = body['transID'],
        payment_method = body['payment_method'],
        amount_paid = order.order_total,
        status = True
    )
    payment.save()
    order.payment = payment
    order.is_ordered = True
    order.save()
    
    
    
    cart_items = CartItem.objects.filter(user=request.user)

    for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.payment = payment
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.product_id
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.price
        orderproduct.ordered = True
        orderproduct.save()
        
        # reduce the quantity in table after ordering the products
        
        product = Product.objects.get(id=item.product_id)
        product.stock -= item.quantity
        product.save()
        
        
        
        
    # clear cart product after ordering
    CartItem.objects.filter(user=request.user).delete()

    # send order number and transaction id back to sendData method via JsonResponse
    data = {
        'order_number' : order.order_number,
        'transID': payment.payment_id,
    }
    
    # account_sid = ('ACe6819c922225f393518734cfe07deebd')
    # auth_token = ('765ca030c76f610974fa611906791d37')
    # client = Client(account_sid, auth_token)
        
    print(request.user.first_name)
    print(payment.payment_id)
    
    

    # message = client.messages.create(
    #                           body = f"Hello {request.user.first_name}, You have successfully ordered on our website.\n\nHere is your Payment ID: {payment.payment_id}\n\nIf you have any trouble, please contact us at 55munavirt@gmail.com.",
    #                           from_='+12705173381',
    #                           to='+916238142442'
    #                       )
    
    
    # print(message.sid)
    
    return JsonResponse(data)


def order_complete(request):
    order_number = request.GET.get('order_number')
    transID = request.GET.get('payment_id')
    

    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        ordered_products = OrderProduct.objects.filter(order_id=order.id)

        subtotal = 0
        for i in ordered_products:
            subtotal += i.product_price * i.quantity
        payment = Payment.objects.get(payment_id=transID)
        context = {
            'order': order,
            'ordered_products': ordered_products,
            'order_number': order_number,
            'transID': payment.payment_id,
            'payment': payment,
            'subtotal': subtotal,
        }

        return render(request, 'order_complete.html', context)
    except Order.DoesNotExist:
        return HttpResponse("Order does not exist.")
    except Payment.DoesNotExist:
        return HttpResponse("Payment does not exist.")
    except Exception as e:
        # Handle any other exceptions
        return HttpResponse(f"An error occurred: {str(e)}")






# def payments_completed(request):
#     order_number = request.GET.get('order_number')
#     transID = request.GET.get('payment_id')
#     try:
#         order = Order.objects.get(order_number = order_number)
#         ordered_products = OrderProduct.objects.filter(order_id=order.id)

#         subtotal = 0
#         for i in ordered_products:
#             subtotal += i.product.offer_price() * i.quantity

#         payment = Payment.objects.get(payment_id=transID)

#         context = {
#             'order': order,
#             'ordered_products': ordered_products,
#             'order_number': order.order_number,
#             'transID': payment.payment_id,
#             'payment': payment,
#             'subtotal': subtotal,
#         }
#         return render(request, 'orders/payment_success.html', context)
#     except (Payment.DoesNotExist, Order.DoesNotExist):
#         return redirect('home')


    
    
    

# def print_invoice(request):
#     # Get the order details
#     order_number = request.GET.get('order_number')
#     transID = request.GET.get('payment_id')
#     print(f"order_number={order_number}")
#     try:
#         order = Order.objects.get(order_number=order_number, is_ordered=True)
#         ordered_products = OrderProduct.objects.filter(order_id=order.id)
#         subtotal = 0
#         for i in ordered_products:
#             subtotal += i.product_price * i.quantity
#         transID = request.GET.get('payment_id') # Get the payment ID from the query params
#         payment = Payment.objects.get(payment_id=transID)
#         context = {
#             'order': order,
#             'ordered_products': ordered_products,
#             'order_number': order_number,
#             'transID': payment.payment_id,
#             'payment': payment,
#             'subtotal': subtotal,
#         }
        
#         # Render the HTML template as a string
#         html_string = render_to_string('invoice.html', context)
        
#         # Generate the PDF file
#         html = HTML(string=html_string)
#         pdf_file = html.write_pdf()
        
#         # Return the PDF file as a response
#         response = HttpResponse(pdf_file, content_type='application/pdf')
#         response['Content-Disposition'] = 'filename="invoice.pdf"'
#         return response
    
#     except Payment.DoesNotExist:
#         return HttpResponse('payment')
     
#     except Order.DoesNotExist:
#         print(f"No order found with order_number={order_number} and is_ordered=True")
#         return HttpResponse('order')




# def order_export_pdf(request, order_number):
#     try:
#         order = Order.objects.get(order_number=order_number, is_ordered=True)
#         ordered_products = OrderProduct.objects.filter(order_id=order.id)

#         subtotal = 0
#         for i in ordered_products:
#             subtotal += i.product_price * i.quantity

#         payment = Payment.objects.get(payment_id=order.payment.payment_id)

#         context = {
#             'order': order,
#             'ordered_products': ordered_products,
#             'order_number': order_number,
#             'transID': payment.payment_id,
#             'payment': payment,
#             'subtotal': subtotal,
#             'css_file': static('css/main.css'),
#         }

#         html_string = render_to_string('invoice_pdf.html', context)
#         html = weasyprint.HTML(string=html_string)
#         pdf_bytes = html.write_pdf()

#         response = HttpResponse(pdf_bytes, content_type='application/pdf')
#         response['Content-Disposition'] = f'attachment; filename=invoice.pdf'
#         return response

#     except (Payment.DoesNotExist, Order.DoesNotExist):
#         return redirect('home')



def coupon(request):
  if request.method == 'POST':
    coupon_code = request.POST['coupon']
    grand_total = request.POST['grand_total']
    coupon_discount = 0
    try:
      instance = UserCoupon.objects.get(user = request.user ,coupon__code = coupon_code)

      if float(grand_total) >= float(instance.coupon.min_value):
        coupon_discount = ((float(grand_total) * float(instance.coupon.discount))/100)
        grand_total = float(grand_total) - coupon_discount
        grand_total = format(grand_total, '.2f')
        coupon_discount = format(coupon_discount, '.2f')
        msg = 'Coupon Applied successfully'
        instance.used = True
        instance.save()
      else:
          msg='This coupon is only applicable for orders more than ₹'+ str(instance.coupon.min_value)+ '\- only!'
    except:
            msg = 'Coupon is not valid'
    response = {
               'grand_total': grand_total,
               'msg':msg,
               'coupon_discount':coupon_discount,
               'coupon_code':coupon_code,
                }

  return JsonResponse(response)





        
        
