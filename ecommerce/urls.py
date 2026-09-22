"""
URL configuration for ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app.views import client_views, admin_views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('admin/', admin.site.urls),
    

    path('dashboard/',
        admin_views.dashboard,
        name='dashboard'
    ),

    path('admin_logout',
         admin_views.admin_logout_view,
         name='admin_logout'
    ),

    path('book_lists/',
        admin_views.book_lists,
        name='book_lists'
    ),

    path('add_book/',
        admin_views.add_book,
        name='add_book'
    ),
    
    path('edit_book/<int:pk>/',
        admin_views.edit_book,
        name='edit_book'
    ),
    
     path('delete_book/<int:pk>/',
        admin_views.delete_book,
        name='delete_book'
    ),

    path('categories/',
         admin_views.categories,
         name='categories'
    ),

    path('add_category/',
        admin_views.add_category,
        name='add_category'
    ),

    path('edit_category/<int:pk>/',
        admin_views.edit_category,
        name='edit_category'
    ),

    path('delete_category/<int:pk>/',
        admin_views.delete_category,
        name='delete_category'
    ),
    
    path('orders/',
         admin_views.orders,
         name='orders'
    ),

    path('order_detail/<int:pk>/',
        admin_views.order_detail,
        name='order_detail'
    ),

    path('update_order/<int:pk>/update/',
        admin_views.update_order,
        name='update_order'
    ),

    path('customers/',
         admin_views.customers,
         name='customers'
    ),

    path('customer_detail/<int:pk>/',
         admin_views.customer_detail,
         name='customer_detail'
    ),

    path('delete_customer/<int:pk>/',
         admin_views.delete_customer,
         name='delete_customer'
    ),

    path('edit_customer/<int:pk>/',
         admin_views.edit_customer,
         name='edit_customer'
    ),

    path('reviews/',
        admin_views.reviews,
        name='reviews'
    ),

    path('review_detail/<int:pk>/',
        admin_views.review_detail,
        name='review_detail'
    ),

    path('reviews/<int:pk>/delete/',
        admin_views.delete_review,
        name='admin_delete_review'
    ),

    path('coupons/',
        admin_views.coupons,
        name='coupons'
    ),

    path('coupons/add/',
        admin_views.add_coupon,
        name='add_coupon'
    ),

    path('coupons/<int:pk>/edit/',
        admin_views.edit_coupon,
        name='edit_coupon'
    ),

    path('coupons/<int:pk>/delete/',
        admin_views.delete_coupon,
        name='delete_coupon'
    ),

    path('reports/',
        admin_views.reports,
        name='reports'
    ),
    path('profile/',
        client_views.profile,
        name='profile'
    ),

    path('edit_profile/',
        client_views.edit_profile,
        name='edit_profile'
    ),

    path('register',
        client_views.register_view,
        name='register'
    ),

    path('login',
        client_views.login_view,
        name='login'
    ),

    path('logout',
        client_views.client_logout_view,
        name='logout'
    ),
    
    path('',
        client_views.index,
        name='index'
    ),

    path("search/",
        client_views.search,
        name="search"
    ),
    
    path('shop/',
        client_views.shop,
        name='shop'
    ),

    path('category/<int:pk>/',
        client_views.category_books,
        name='category_books'
    ),
    
    path('category/',
        client_views.category,
        name='category'
    ),

    path('book_by_category/<int:category_id>',
        client_views.book_by_category,
        name='book_by_category'
    ),
        
    path('book_detail/<int:pk>/',
        client_views.book_detail,
        name='book_detail'
    ),

    path('featured_books/',
        client_views.featured_books,
        name='featured_books'
    ),

    path('best_sellers/',
        client_views.best_sellers,
        name='best_sellers'
    ),

    path('new_arrival/',
        client_views.new_arrival,
        name='new_arrival'
    ),

    path("delete_profile/",
        client_views.delete_profile,
        name="delete_profile"
    ),

    path('add_to_cart/<int:book_id>/',
         client_views.add_to_cart,
         name='add_to_cart'
    ),

    path('cart/',
         client_views.cart_view,
         name='cart'
    ),

    path('increase_quantity/<int:item_id>/',
        client_views.increase_quantity,
        name='increase_quantity'
    ),

    path('decrease_quantity/<int:item_id>/',
         client_views.decrease_quantity,
         name='decrease_quantity'
    ),

    path('remove_item/<int:item_id>/',
         client_views.remove_item,
         name='remove_item'
    ),
    
    path('checkout/',
         client_views.checkout,
         name='checkout'
    ),

    path('my-orders/',
        client_views.my_orders,
        name='my_orders'
    ),
    
    path('my_order_detail/<int:order_id>/',
        client_views.my_order_detail,
        name='my_order_detail'
    ),

    path('order/<int:order_id>/',
        client_views.cancel_order,
        name='cancel_order'
    ),

    path('submit-review/<int:pk>/',
        client_views.submit_review,
        name='submit_review'
    ),

    path('review/update/<int:pk>/',
        client_views.update_review,
        name='update_review'
    ),

    path('review/delete/<int:pk>/',
        client_views.delete_review,
        name='delete_review'
    ),

    path('wishlist/add/<int:book_id>/',
        client_views.add_to_wishlist,
        name='add_to_wishlist'
    ),

    path('wishlist/remove/<int:book_id>/',
        client_views.remove_from_wishlist,
        name='remove_from_wishlist'
    ),

    path('my-wishlist/',
        client_views.my_wishlist,
        name='my_wishlist'
    ),

    path('about/',
        client_views.about,
        name='about'
    ),



]+static(settings.STATIC_URL,document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

