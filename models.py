from django.db import models
from django.contrib.auth.models import User

from django.utils import timezone


# Create your models here.
from django.db import models

class user(models.Model):
    staff_id = models.IntegerField()
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    phno = models.IntegerField()

    def __str__(self):
        return self.username


class LoginData(models.Model):
    username=models.CharField(max_length=50)
    password=models.CharField(max_length=50)

class PasswordReset(models.Model):
    user=models.ForeignKey(user,on_delete=models.CASCADE)
    token=models.CharField(max_length=4)


from django.db import models


from django.db import models


class Selling(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    seller = models.ForeignKey(user, on_delete=models.CASCADE)
    property_type = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    price = models.IntegerField()
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    title = models.CharField(max_length=100)
    area = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='selling_images/')
    aadhaar_number = models.CharField(max_length=12)
    is_active = models.BooleanField(default=False)  # Only visible after approval
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    # created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.status})"


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    property = models.ForeignKey(Selling, on_delete=models.CASCADE)
    added_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'property')  # Prevent duplicates
class ContactAgent(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    message = models.TextField()
    property = models.ForeignKey('Selling', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
        # return f"{self.name} - {self.property}"

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"


# models.py

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings  # For accessing email settings

from django.db import models
from django.contrib.auth.models import User

from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name


class Property(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('BOOKED', 'Booked'),
        ('SOLD', 'Sold'),
        ('REJECTED', 'Rejected'),
    ]

    PROPERTY_TYPE_CHOICES = [
        ('APARTMENT', 'Apartment'),
        ('VILLA', 'Villa'),
        ('PLOT', 'Plot'),
        ('HOUSE', 'House'),
        ('COMMERCIAL', 'Commercial'),
        ('OTHER', 'Other'),
    ]

    title = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    image = models.ImageField(upload_to='properties/', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    sold = models.BooleanField(default=False)  # ✅ Track if sold
    property_type = models.CharField(
        max_length=50,
        choices=PROPERTY_TYPE_CHOICES,
    )

    seller = models.ForeignKey(user, on_delete=models.CASCADE, related_name='properties_sold')
    buyer = models.ForeignKey(user, on_delete=models.SET_NULL, null=True, blank=True, related_name='properties_bought')

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title




from django.db import models
from django.contrib.auth.models import User






# class PropertyImage(models.Model):
#      property = models.ForeignKey('Property', on_delete=models.CASCADE, related_name='images')
#      image = models.ImageField(upload_to='property_images/')
#
#      def __str__(self):
#          return f"Image for {self.property.title}"


class TokenWallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tokens = models.PositiveIntegerField(default=100)

    def __str__(self):
        return f"{self.user.username} - {self.tokens} tokens"










# Extend User (or use a Profile model)
class Profile(models.Model):
    user = models.OneToOneField(user, on_delete=models.CASCADE)
    tokens = models.DecimalField(default=1000, max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.user.username}'s Profile"

# models.py
from django.db import models
from django.contrib.auth.models import User

class Payment(models.Model):
    STATUS_CHOICES = [
        ('SUCCESS', 'Success'),
        ('FAILED', 'Failed'),
        ('REFUNDED', 'Refunded'),
    ]

    user = models.ForeignKey(user, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.SET_NULL, null=True, blank=True)
    payment_id = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='SUCCESS')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - ₹{self.amount} - {self.status}"


class UserPurchasedProperty(models.Model):
    user = models.ForeignKey(user, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(auto_now_add=True)
    amount_paid = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=50, default='Purchased')  # Purchased, Refund Requested, Refunded

    def __str__(self):
        return f"{self.user.username} - {self.property.title}"


from django.db import models
from django.contrib.auth.models import User

class RefundRequest(models.Model):
    user = models.ForeignKey(user, on_delete=models.CASCADE)
    purchased_property = models.ForeignKey('UserPurchasedProperty', on_delete=models.CASCADE)
    reason = models.TextField()
    status = models.CharField(max_length=20, default='Pending')  # Pending, Approved, Rejected
    amount_paid = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    refund_id = models.CharField(max_length=100, blank=True, null=True)  # Razorpay refund ID

    def __str__(self):
        return f"RefundRequest({self.user.username}, {self.purchased_property.property.title})"
