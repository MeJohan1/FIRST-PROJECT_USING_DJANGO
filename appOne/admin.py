from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django import forms
from django.contrib import admin
from .models import Reservation
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

#Created by Leandro Felix, Johan Ahmed Chowdhury and Mahathir Saad Islam
# provide feedback from team members



class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'is_active')

class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User
        fields = fields = ('username', 'first_name', 'last_name', 'email', 'is_active', 'is_staff', 'is_superuser')

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser'),
        }),
    )

try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass

admin.site.register(User, CustomUserAdmin)

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'user__is_active', 'surname', 'date_of_birth', 'email', 'phone_number')
    list_filter = ('user__is_active',)

    def user__is_active(self, obj):
        return obj.user.is_active
    user__is_active.boolean = True
    user__is_active.admin_order_field = 'user__is_active'



@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('user', 'booking_start_date', 'booking_end_date', 'status')
    list_filter = ('status', 'booking_start_date')
    actions = ['approve_reservations', 'reject_reservations']

    def approve_reservations(self, request, queryset):
        queryset.update(status='approved')
        self.message_user(request, "Selected reservations have been approved.")
    approve_reservations.short_description = "Approve selected reservations"

    def reject_reservations(self, request, queryset):
        queryset.update(status='rejected')
        self.message_user(request, "Selected reservations have been rejected.")
    reject_reservations.short_description = "Reject selected reservations"


admin.site.register(Cart)

admin.site.register(Equipment)
