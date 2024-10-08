# Generated by Django 4.2.11 on 2024-04-25 08:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Equipment",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("type_of_device", models.CharField(max_length=255)),
                ("image", models.ImageField(upload_to="appOne/images/")),
                ("quantity", models.PositiveIntegerField()),
                (
                    "audit",
                    models.DateField(
                        help_text="Please enter the date in YYYY-MM-DD format."
                    ),
                ),
                ("device_name", models.CharField(max_length=255)),
                ("status", models.CharField(max_length=255)),
                ("comments", models.TextField(blank=True, null=True)),
                ("location", models.CharField(max_length=255)),
                ("onsite", models.BooleanField(default=True)),
                ("availability", models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name="Reservation",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("booking_start_date", models.DateTimeField()),
                ("booking_end_date", models.DateTimeField()),
                ("alerts", models.TextField(blank=True, null=True)),
                (
                    "status",
                    models.CharField(
                        blank=True,
                        choices=[("approved", "Approved"), ("rejected", "Rejected")],
                        max_length=255,
                        null=True,
                    ),
                ),
                ("purpose", models.TextField()),
                (
                    "equipment",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="reservations",
                        to="appOne.equipment",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="reservations",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Person",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=30)),
                ("surname", models.CharField(max_length=30)),
                ("date_of_birth", models.DateField(verbose_name="date of birth")),
                (
                    "email",
                    models.EmailField(
                        max_length=254, unique=True, verbose_name="email address"
                    ),
                ),
                (
                    "phone_number",
                    models.CharField(max_length=17, verbose_name="phone number"),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Cart",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("booking_start_date", models.DateTimeField()),
                ("booking_end_date", models.DateTimeField()),
                ("purpose", models.TextField()),
                (
                    "equipment",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="cart_items",
                        to="appOne.equipment",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="carts",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
