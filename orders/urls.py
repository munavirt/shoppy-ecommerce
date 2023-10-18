from django.urls import path, include
from . import views
 


urlpatterns = [
    path('place_order/',views.place_order,name='place_order'),
    # path('print-invoice/<str:order_number>/', views.print_invoice, name='print_invoice'),
    # path('print-invoice', views.print_invoice, name='print_invoice'),
    # path('order_export_pdf/<str:order_number>/', views.order_export_pdf, name='order_export_pdf'), mian
    path('payments/',views.payments,name='payments'),
    # path('paypal/', views.paypal, name='paypal'),
    # path('razorpay/', views.razorpay, name='razorpay'),
    path('order_complete/',views.order_complete,name = 'order_complete'),
]