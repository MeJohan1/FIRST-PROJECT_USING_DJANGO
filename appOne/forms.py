from django import forms
from datetime import date
from django.forms import ModelForm, DateInput
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError  # Ensure this import is added
from .models import *


# Created by Johan Ahmed Chowdhury, w1910565 and Mahathir Saad Islam
# provide feedback from team members
class EquipmentFilterForm(forms.ModelForm):
    equipment_id = forms.IntegerField(required=False)
    type_of_device = forms.CharField(required=False)
    class Meta:
        model = Equipment
        fields = ['equipment_id', 'type_of_device']



class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = '__all__'
        widgets = {
            'audit': DateInput(attrs={'type': 'date'}),
        }
        error_messages = {
            'audit': {
                'invalid': "Please enter a valid date (YYYY-MM-DD).",
            },
        }

    def clean_audit(self):
        audit = self.cleaned_data.get('audit')
        if audit and audit > date.today():
            raise ValidationError("Audit date cannot be in the future.")
        return audit




class SignUpForm(UserCreationForm):
    name = forms.CharField(max_length=30)
    surname = forms.CharField(max_length=30)
    date_of_birth = forms.DateField(help_text='Format: YYYY-MM-DD')
    email = forms.EmailField()
    phone_number = forms.CharField(max_length=17)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'name', 'surname', 'date_of_birth', 'phone_number']

    def clean_date_of_birth(self):
        dob = self.cleaned_data['date_of_birth']
        if dob >= date.today():
            raise ValidationError("The date of birth cannot be in the future or this year.")
        return dob

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.first_name = self.cleaned_data['name']
        user.last_name = self.cleaned_data['surname']
        user.email = self.cleaned_data['email']
        user.date_of_birth = self.cleaned_data['date_of_birth']
        user.phone_number = self.cleaned_data['phone_number']
        user.is_active = False

        if commit:
            user.save()
            Person.objects.create(
            user=user,
            name=user.first_name,
            surname=user.last_name,
            date_of_birth=self.cleaned_data['date_of_birth'],
            email=user.email,
            phone_number=self.cleaned_data['phone_number']
        )
        return user




class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['booking_start_date', 'booking_end_date', 'purpose']
        widgets = {
            'booking_start_date': forms.DateInput(attrs={'type': 'date'}),
            'booking_end_date': forms.DateInput(attrs={'type': 'date'}),
        }
