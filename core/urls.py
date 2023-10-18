from django.urls import path
from . import views



urlpatterns = [
    path('',views.home,name='home'),
    path('blog/',views.blog,name='blog'),
    path('checkout/',views.checkout,name='checkout'),
    path('confirmation/',views.confirmation,name='confirmation'),
    path('contact/',views.contact_us,name='contact_us'),
    path('elements/',views.elements,name='elements'),
    path('tracking/',views.tracking,name='tracking'),
    path('single_blog/',views.single_blog,name='single_blog'),
    path('cp_register/',views.cp_register,name='cp_register'),
    path('cp_login/',views.cp_login, name='cp_login'),
    
     path('activate/<uidb64>/<token>/', views.cp_activate, name='cp_activate'),
     path('cp_register/cp_login/', views.cp_login, name='cp_login_email'),
     
     path('api/',views.api_call,name='api')
    
    
]