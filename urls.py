"""
URL configuration for property project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path,include
from app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.log, name='login'),
    path('signup/', views.signup, name='signup'),
    path('edit_profile/',views.edit_profile,name='edit_profile'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('user_dashboard/', views.user_dashboard, name='user_dashboard'),  # ✅ this is crucial
    path('home', views.index, name='home'),
    path('properties/', views.properties, name='properties'),
    path('property/<int:property_id>', views.property_details, name='property_details'),
    path('services/',views.services,name='services'),
    path('contact',views.contact),
    path('about/',views.about,name='about'),
    path('signup',views.signup),
    path('admin_properties',views.admin_properties),
    path('user',views.user),
    path('forgot_password/',views.forgot_password,name='forgot_password'),
    path('reset/<str:token>/', views.reset_password, name='reset_password'),
    # path('payment',views.pay),
    # path('add_properties',views.add_properties),
    # path('admin.buy_property',views.admin.buy_property),
    path('admin_contact',views.admin_contact),
    path('properties_list',views.properties_list),
    # path('listing',views.listing),
    # path('buy_properties',views.buy_properties),
    # path('sell_properties',views.sell_properties),
    path('contact_agent',views.contact_agent),
    path('contact/', views.contact, name='contact'),
    path('delete-sell/<int:id>/', views.delete_selling, name='delete_selling'),  # ✅ must match URL
    path('admin_user',views.users),
    path('delete_property/<int:id>/', views.delete_property, name='delete_property'),
    # path("property/<int:pk>/buy/", views.buy_property, name="buy_property"),
    # path('payment/<int:property_id>/', views.payment, name='payment'),
    # path('pay/<int:property_id>/', views.pay, name='pay'),
    path('payment/<int:property_id>/', views.pay, name='payment'),
    # path('payment_success/', views.payment_success, name='payment_success'),
    path('admin_dashboard', views.admin_dashboard, name='admin_dashboard'),
    path('add_property', views.add_property, name='add_property'),
    path('buy_properties/', views.buy_properties, name='buy_properties'),
    # path('sell_list', views.sell_list, name="sell_list"),
    # path('admin_property_list', views.admin_property_list),
    # path('admin/property-status/<int:prop_id>', views.update_property_status, name="update_property_status"),
    # path('update_property_status/<int:prop_id>/', views.update_property_status, name='update_property_status'),
    path('add-to-wishlist/<int:property_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('pay/<int:property_id>/', views.pay, name='pay'),
    path('payment_success/', views.payment_success),
    path('payment-history/', views.payment_history, name='payment_history'),
    path('refund_request_submit/', views.refund_request_submit, name='refund_request_submit'),
    path('admin_approve_refund/<int:refund_id>/', views.admin_approve_refund, name='admin_approve_refund'),
    path('admin_reject_refund/<int:refund_id>/', views.admin_reject_refund, name='admin_reject_refund'),
    # path('add-sell/', views.add_sell, name='add-sell'),
    # path('sell-list/', views.sell_listing, name='sell_list'),
    # path('admin-properties/', views.admin_property_list, name='admin_property_list'),
    # path('admin/property-status/<int:prop_id>/', views.update_property_status, name='update_property_status'),
    path('update_property_status/<int:selling_id>/', views.update_property_status, name='update_property_status'),
    # path('selling_requests_view/',views.selling_requests_view,name='selling_requests_view'),
    path('selling_create/',views.selling_create,name='selling_create'),
    path('edit_property/',views.edit_property,name='edit_property'),
    path('practise',views.practise)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)








