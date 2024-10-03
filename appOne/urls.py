from django.contrib.auth.views import LoginView, LogoutView
from appOne import views
from .models import Equipment
from appOne.forms import EquipmentFilterForm
from django.urls import path, include
from django.views.decorators.cache import never_cache
from django.contrib import admin
from .views import CustomLoginView, CustomLogoutView
from .views import AdminLoginView
from .views import approve_user

# Created by team members

CustomLoginView = never_cache(views.CustomLoginView.as_view())
CustomLogoutView = never_cache(views.CustomLogoutView.as_view())

urlpatterns = [

    path("", views.welcomePage, name="welcomepage"),
    path('homePage/', views.homepage, name="homepage"),
    path("contact-us/", views.contactUsPage, name="contact_us"),
    path("Wel_contact-us/", views.contactUsPageWel, name="Wel_contact_us"),
    path('equipment-list/', views.equipmentList, name='equipment_list'),
    path('equipment/add/', views.equipment_add, name='equipment_add'),
    path('equipment/<int:equipment_id>/edit/', views.equipment_edit, name='equipment_edit'),
    path('equipment/<int:equipment_id>/delete/', views.equipment_delete, name='equipment_delete'),
    path('equipment/<int:pk>/', views.equipment_detail, name='equipment_detail'),
    path('equipment/<int:pk>/reserve/', views.equipment_reserve, name='equipment_reserve'),
    path('add-to-cart/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/remove/<int:pk>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:pk>/', views.update_cart_item, name='update_cart_item'),
    path('cart/place-booking/', views.place_booking, name='place_booking'),
    path('cart/place-booking/', views.equipment_reserve, name='place_booking'),
    path('register/', views.register, name='register'),
    path('login/', CustomLoginView, name='login'),
    path('custom-admin/login/', AdminLoginView.as_view(), name='custom_admin_login'),
    path('logout/', CustomLogoutView, name='logout'),
    path('user/orders/', views.user_orders, name='user_orders'),
    path('cancel-reservation/<int:reservation_id>/', views.cancel_reservation, name='cancel_reservation'),
    path('management/', views.all_users, name='management'),
    path('management/add-user/', views.add_user, name='add_user'),
    path('management/edit-user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('management/delete-user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('management/approve-user/<int:user_id>/', views.approve_user, name='approve_user'),
    path('approve_user/<int:user_id>/', approve_user, name='approve_user'),
    path('manage-booking/', views.view_reservations, name='manage_booking'),
    path('manage_booking/approve-reservation/<int:reservation_id>/', views.approve_reservation, name='approve_reservation'),
    path('manage_booking/reject-reservation/<int:reservation_id>/', views.reject_reservation, name='reject_reservation'),
    path('reports/', views.generate_report, name='generate_report'),
    path('about/', views.about_view, name='about'),
    path('help/', views.help_view, name='help'),
    path('my-account/', views.my_account, name='my_account'),

]
