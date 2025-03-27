from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_user, name='login'),
    path('register/', views.register_user, name='register'),
    path('home/', views.home, name='home'),
    path('models/2d/', views.models_2d, name='models_2d'),
    path('models/3d/', views.models_3d, name='models_3d'),
    path('products/3d/<int:pk>', views.products_3d, name='products_3d'),
    path('products/2d/<int:pk>', views.products_2d, name='products_2d'),
    path('single_product/3d/<int:pk>', views.single_product_3d, name='single_product_3d'),
    path('single_product/2d/<int:pk>', views.single_product_2d, name='single_product_2d'),
    path('logout/', views.logout_user, name='logout'),
    path('order/<str:product_type>/<int:pk>/', views.order_product, name='order_product'),
    path('order/success/', views.order_success, name='order_success'),
    path('feedback/', views.feedback_list, name='feedback_list'),
    path('feedback/submit/', views.submit_feedback, name='submit_feedback'),
    path('about/',views.about,name='about'),
    path('like-product/<str:product_type>/<int:product_id>/', views.like_product, name='like_product'),
    path('cart/', views.liked_products, name='cart'),
]
