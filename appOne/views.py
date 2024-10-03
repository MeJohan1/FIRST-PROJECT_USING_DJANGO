from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView, LogoutView
from django.core.exceptions import ValidationError
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.timezone import now
from django.views.decorators.cache import never_cache
from .forms import EquipmentFilterForm, EquipmentForm, ReservationForm, SignUpForm
from .models import Equipment, Reservation, User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse
from .models import*
from .forms import EquipmentFilterForm
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseForbidden
from django.core.exceptions import ValidationError
from .forms import*
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.utils.timezone import now
from django.utils.timezone import now, timedelta
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import SignUpForm
from .admin import CustomUserChangeForm
from django.contrib.auth.models import User
from django.shortcuts import render
from django.db.models import Count
from .models import Equipment

#created by team members

# Helper functions for user checks
def admin_check(user):
    return user.is_authenticated and user.is_staff

def is_not_authenticated(user):
    return not user.is_authenticated

# Admin views
@user_passes_test(admin_check)
def some_admin_view(request):
    return render(request, 'admin/login.html')

@user_passes_test(is_not_authenticated, login_url='homepage', redirect_field_name=None)
def welcomePage(request):
    if request.user.is_authenticated:
        return redirect('homepage')
    return render(request, "appOne/welcomePage.html")

@login_required
def homePage(request):
    return render(request, "appOne/home.html")

@login_required
def contactUsPage(request):
    return render(request, "appOne/contactus.html")


# Equipment handling
@login_required
def equipmentList(request):
    form = EquipmentFilterForm(request.GET or None)
    equipments = Equipment.objects.all()
    if form.is_valid():
        equipment_id = form.cleaned_data.get('equipment_id')
        type_of_device = form.cleaned_data.get('type_of_device')
        if equipment_id:
            equipments = equipments.filter(id=equipment_id)
        if type_of_device:
            equipments = equipments.filter(type_of_device__icontains=type_of_device)
    onsite_filter = request.GET.get('onsite')
    type_filter = request.GET.get('type_of_device')
    if onsite_filter:
        equipments = equipments.filter(onsite=onsite_filter == 'True')
    if type_filter:
        equipments = equipments.filter(type_of_device__icontains=type_filter)
    sort_by = request.GET.get('sort_by')
    if sort_by == 'a_to_z':
        equipments = equipments.order_by('device_name')
    elif sort_by == 'z_to_a':
        equipments = equipments.order_by('-device_name')
    search_term = request.GET.get('search_term', '').strip()
    if search_term:
        equipments = equipments.filter(device_name__icontains=search_term)
    context = {'filter_form': form, 'equipment_list': equipments}
    return render(request, 'appOne/equipmentList.html', context)

@user_passes_test(admin_check)
def equipment_add(request):
    if request.method == 'POST':
        form = EquipmentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Equipment added successfully.")
            return redirect('equipment_list')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = EquipmentForm()
    return render(request, 'appOne/equipment_form.html', {'form': form, 'equipment': None})

@user_passes_test(admin_check)
def equipment_edit(request, equipment_id):
    # Admin edit existing equipment
    equipment = get_object_or_404(Equipment, pk=equipment_id)
    if request.method == 'POST':
        form = EquipmentForm(request.POST, request.FILES, instance=equipment)
        if form.is_valid():
            form.save()
            return redirect('equipment_list')
    else:
        form = EquipmentForm(instance=equipment)
    return render(request, 'appOne/equipment_form.html', {'form': form, 'equipment': equipment})

@user_passes_test(admin_check)
def equipment_delete(request, equipment_id):
    # Admin view to delete equipments
    equipment = get_object_or_404(Equipment, pk=equipment_id)
    equipment.delete()
    messages.success(request, "Equipment successfully deleted!")
    return redirect('equipment_list')

@login_required
def equipment_detail(request, pk):
    # View to show details
    equipment = get_object_or_404(Equipment, pk=pk)
    reservation_form = ReservationForm(request.POST or None)
    if request.method == 'POST':
        if 'add_to_cart' in request.POST:
            cart = request.session.get('cart', {})
            reservation_details = {
                'booking_start_date': request.POST['booking_start_date'],
                'booking_end_date': request.POST['booking_end_date'],
                'purpose': request.POST['purpose'],
                'user': request.user.id
            }
            cart[str(equipment.id)] = reservation_details
            request.session['cart'] = cart
            messages.success(request, "Item added to cart.")
            return redirect('equipment_list')
        elif reservation_form.is_valid():
            pass
    return render(request, 'appOne/equipment_detail.html', {'equipment': equipment, 'form': reservation_form})

# User registrations and login
@never_cache
def register(request):
    if request.user.is_authenticated:
        return redirect('homepage')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Account created for {user.username}!')
            return redirect('login')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = SignUpForm()
    return render(request, 'user/register.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'user/login.html'

    def get_success_url(self):
        return reverse_lazy('homepage')

    def form_valid(self, form):
        return super().form_valid(form)

class AdminLoginView(LoginView):
    template_name = 'user/adminlogin.html'
    def get_success_url(self):
        return reverse_lazy('homepage')
    def form_valid(self, form):
        if not form.get_user().is_staff:
            return redirect('login')
        return super().form_valid(form)

class CustomLogoutView(LogoutView):
    next_page = 'welcomepage'

# Cart handling
@login_required
def view_cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    for pk, reservation_details in cart.items():
        try:
            equipment = Equipment.objects.get(pk=pk)
            user = request.user
            cart_items.append({
                'equipment': equipment,
                'start_date': reservation_details['booking_start_date'],
                'end_date': reservation_details['booking_end_date'],
                'purpose': reservation_details['purpose'],
                'user': user.username
            })
        except Equipment.DoesNotExist:
            messages.error(request, f'An item in your cart could not be found.')
            continue
        except KeyError:
            messages.error(request, f'Incomplete reservation details for some items.')
            continue
    past_reservations = Reservation.objects.filter(user=request.user, status='approved').select_related('equipment')
    past_reservations = [res for res in past_reservations if res.equipment and res.equipment.id]
    return render(request, 'appOne/cart.html', {
        'cart_items': cart_items,
        'past_reservations': past_reservations
    })

def add_to_cart(request, pk):
    # Add an item cart
    if request.method == 'POST':
        try:
            equipment = Equipment.objects.get(pk=pk)
            booking_start_date = request.POST.get('booking_start_date')
            booking_end_date = request.POST.get('booking_end_date')
            purpose = request.POST.get('purpose')
            cart_item, created = Cart.objects.get_or_create(
                user=request.user,
                equipment=equipment,
                defaults={
                    'booking_start_date': booking_start_date,
                    'booking_end_date': booking_end_date,
                    'purpose': purpose
                }
            )
            if not created:
                cart_item.booking_start_date = booking_start_date
                cart_item.booking_end_date = booking_end_date
                cart_item.purpose = purpose
                cart_item.save()
            messages.success(request, f'Added {equipment.device_name} to your cart.')
            return redirect('equipment_list')
        except Equipment.DoesNotExist:
            messages.error(request, 'This item does not exist.')
            return redirect('equipment_list')

def remove_from_cart(request, pk):
    # Remove an items from the cart
    cart = request.session.get('cart', {})
    if str(pk) in cart:
        del cart[str(pk)]
        request.session['cart'] = cart
        messages.success(request, "Item removed from cart.")
    else:
        messages.error(request, "Item not in cart.")
    return redirect('view_cart')

@login_required
def update_cart_item(request, pk):
    # Update  of a cart items
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        start_date = request.POST.get('booking_start_date')
        end_date = request.POST.get('booking_start_date')
        purpose = request.POST.get('purpose')
        if pk in cart:
            cart[pk] = {'quantity': 1, 'start_date': start_date, 'end_date': end_date, 'purpose': purpose}
            request.session['cart'] = cart
            messages.success(request, "Cart updated successfully.")
        else:
            messages.error(request, "Item not in cart.")
        return redirect('view_cart')

# Equipment booking handling
@login_required
def equipment_reserve(request, pk):
    equipment = get_object_or_404(Equipment, pk=pk)
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user
            reservation.equipment = equipment
            reservation.save()
            messages.success(request, "Reservation successfully created.")
            return redirect('equipment_list')
        else:
            return render(request, 'appOne/equipment_detail.html', {'form': form, 'equipment': equipment})
    else:
        form = ReservationForm()
        return render(request, 'appOne/equipment_detail.html', {'equipment': equipment, 'form': form})

@login_required
def place_booking(request):
    # Place multiple book from cart
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        if not cart:
            messages.error(request, "No items in your cart.")
            return redirect('view_cart')
        for equipment_id, reservation_details in cart.items():
            try:
                equipment = Equipment.objects.get(pk=equipment_id)
                Reservation.objects.create(
                    equipment=equipment,
                    user=request.user,
                    booking_start_date=reservation_details['booking_start_date'],
                    booking_end_date=reservation_details['booking_end_date'],
                    purpose=reservation_details['purpose'],
                )
            except Equipment.DoesNotExist:
                messages.error(request, f"Equipment with id {equipment_id} does not exist.")
                continue
            except KeyError as e:
                messages.error(request, f"Missing reservation detail: {e}")
                continue
        request.session['cart'] = {}
        request.session.modified = True  # Ensure the session is marked as modified
        messages.success(request, "All bookings placed successfully.")
        return redirect('equipment_list')
    else:
        return redirect('view_cart')

# User reservation handling
@login_required
def user_orders(request):
    user_reservations = Reservation.objects.filter(user=request.user)
    for reservation in user_reservations:
        reservation.is_overdue = now() >= reservation.booking_end_date
        if not reservation.is_overdue:
            reservation.days_left = (reservation.booking_end_date - now()).days
        else:
            reservation.days_left = -1
    context = {'reservations': user_reservations}
    return render(request, 'user/user_orders.html', context)

@login_required
def cancel_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)
    if not reservation.is_overdue and (reservation.status != 'approved' or not reservation.status):
        reservation.delete()
        messages.success(request, "Reservation cancelled successfully.")
    else:
        messages.error(request, "You cannot cancel this reservation as it is either approved or overdue.")
    return redirect('user_orders')

@user_passes_test(admin_check)
def list_users(request):
    users = User.objects.all()
    return render(request, 'appOne/user_list.html', {'users': users})

@user_passes_test(admin_check)
def add_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'New user {user.username} added successfully!')
            return redirect('list_users')
    else:
        form = SignUpForm()
    return render(request, 'user/add_user.html', {'form': form})

# Admin to delete  user
@user_passes_test(admin_check)
def delete_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user.delete()
    messages.success(request, "User deleted successfully.")
    return redirect('list_users')

# Admin to approve new book
@user_passes_test(admin_check)
def authorize_reservations(request):
    pending_reservations = Reservation.objects.filter(status='pending')
    if request.method == 'POST':
        reservation_id = request.POST.get('reservation_id')
        reservation = get_object_or_404(Reservation, pk=reservation_id)
        reservation.status = 'approved'
        reservation.save()
        messages.success(request, "Reservation approved successfully.")
        return redirect('authorize_reservations')
    return render(request, 'appOne/authorize_reservations.html', {'reservations': pending_reservations})

@login_required
def homepage(request):
    is_admin = request.user.is_staff
    context = {'is_admin': is_admin}
    return render(request, "appOne/home.html", context)

@login_required
def my_account(request):
    context = {
        'is_admin': request.user.is_staff,
        'user': request.user,
    }
    return render(request, 'appOne/account.html', context)

def about_view(request):
    return render(request, 'appOne/about.html')

def help_view(request):
    return render(request, 'appOne/help.html')

@login_required
@user_passes_test(admin_check)
def all_users(request):
    active_users = User.objects.filter(is_active=True).order_by('-date_joined')
    pending_users = User.objects.filter(is_active=False).order_by('-date_joined')
    return render(request, 'appOne/management.html', {'users': active_users, 'pending_users': pending_users})

@login_required
@user_passes_test(admin_check)
def approve_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_active = True
    user.save()
    messages.success(request, "User approved successfully")
    return redirect('management')

# add new user by admin
@login_required
@user_passes_test(admin_check)
def add_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'New user {user.username} added successfully!')
            return redirect('management')
    else:
        form = SignUpForm()
    return render(request, 'appOne/add_user.html', {'form': form})

#Admin to delete users
@login_required
@user_passes_test(admin_check)
def delete_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        user.delete()
        messages.success(request, "User deleted successfully.")
        return redirect('management')
    return redirect('management')

#Admin to update user account, roles
@login_required
@user_passes_test(admin_check)
def edit_user(request, user_id):
    user = User.objects.get(pk=user_id)
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "User updated successfully.")
            return redirect('management')
    else:
        form = CustomUserChangeForm(instance=user)
    return render(request, 'appOne/edit_user.html', {'form': form})

# reservations
@login_required
def view_reservations(request):
    status_filter = request.GET.get('status_filter', 'pending')
    if status_filter == 'all':
        reservations = Reservation.objects.all().order_by('-booking_start_date')
    else:
        reservations = Reservation.objects.filter(status=status_filter).order_by('-booking_start_date')
    return render(request, 'appOne/manage_booking.html', {'reservations': reservations})

#approve ou reject reservations
@login_required
@user_passes_test(admin_check)
@require_http_methods(["POST"])
def approve_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    reservation.status = 'approved'
    reservation.save()
    messages.success(request, "Booking approved")
    return redirect('manage_booking')

@login_required
@user_passes_test(admin_check)
@require_http_methods(["POST"])
def reject_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    reservation.status = 'rejected'
    reservation.save()
    messages.success(request, "Booking rejected")
    return redirect('manage_booking')

@login_required
@user_passes_test(admin_check)
def reports(request):
    return render(request, 'appOne/reports.html')

def generate_report(request):
    inventory_count = Equipment.objects.count()
    overdue_count = Equipment.objects.filter(status='overdue').count()
    equipment_by_category = Equipment.objects.exclude(type_of_device__isnull=True).values('type_of_device').annotate(count=Count('type_of_device'))

    context = {
        'inventory_count': inventory_count,
        'overdue_count': overdue_count,
        'equipment_by_category': equipment_by_category,
    }

    return render(request, 'appOne/report_page.html', context)



def contactUsPageWel(request):
    return render(request, "appOne/contactusWel.html")
