from django.urls import path
from . import views


# from orders.views import print_invoice

urlpatterns = [
    path('register/',views.register,name='register'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('register/login/', views.login, name='login_email'),
    path('forgotPassword/',views.forgot_password,name="forgotPassword"),
    path('resetpassword_validate/<uidb64>/<token>/', views.resetpassword_validate, name='resetpassword_validate'),
     path('resetPassword/', views.resetPassword, name='resetPassword'),
    
    path('dashboard/',views.dashboard,name='dashboard'),
    path('my_orders/',views.my_orders,name='my_orders'),
    path('edit_profile/',views.edit_profile,name='edit_profile'),
    path('change_password/',views.change_password,name='change_password'),
    path('order_detail/<int:order_id>/',views.order_detail,name='order_detail'),
    
    #  path('print-invoice/<str:order_number>/', views.print_invoice, name='print_invoice'),    
]