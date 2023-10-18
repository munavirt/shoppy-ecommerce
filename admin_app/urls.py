from django.urls import path
from . import views

urlpatterns = [
    path('admin_login/',views.admin_login,name='admin_login'),
    path('admin_logout/',views.admin_logout,name='admin_logout'),
    path('dashboard/', views.dashboard,name='admin_dasboard'),
    path('admin_product/', views.admin_product, name='admin_product'),
    path('admin_addProduct/',views.admin_addProduct,name='admin_addProduct'),
    
    path('admin_category',views.adminCategory,name='admin_category'),

    path('admin_messages',views.adminMessages,name='adminMessages'),
    path('delete_message/<int:id>',views.deleteMessage,name='deleteMessage'),
    path('reply_message',views.replyMessage,name='replyMessage'),
]