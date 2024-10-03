from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone


# Mahathir Saad Islam, w1907417
# Help few things by team members.

class Person(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    date_of_birth = models.DateField(verbose_name='date of birth')
    email = models.EmailField(verbose_name='email address', unique=True)
    phone_number = models.CharField(verbose_name='phone number', max_length=17)

    def __str__(self):
        return f"{self.name} {self.surname}"

class Equipment(models.Model):
    id = models.AutoField(primary_key=True)
    type_of_device = models.CharField(max_length=255)
    image = models.ImageField(upload_to='appOne/images/')
    quantity = models.PositiveIntegerField()
    audit = models.DateField(help_text="Please enter the date in YYYY-MM-DD format.")
    device_name = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    comments = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=255)
    onsite = models.BooleanField(default=True)
    availability = models.BooleanField(default=True)

    def __str__(self):
        return f"Equipment {self.id}"

class Reservation(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations',blank=True, null=True)
    booking_start_date = models.DateTimeField()
    booking_end_date = models.DateTimeField()
    alerts = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=255, choices=[('pending', 'Pending'),('approved', 'Approved'), ('rejected', 'Rejected')],default='pending')
    purpose = models.TextField()
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name='reservations', blank=False, null=False)
    def __str__(self):
        return f"Reservation {self.id}"


class Cart(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts')
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name='cart_items')
    booking_start_date = models.DateTimeField()
    booking_end_date = models.DateTimeField()
    purpose = models.TextField()


    def __str__(self):
        return f"Cart {self.id} of {user.first_name} {user.last_name}"
