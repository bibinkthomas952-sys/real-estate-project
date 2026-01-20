from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from.models import *
from django.utils.crypto import get_random_string
from django.conf import settings
import razorpay
from .models import Selling,ContactAgent
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives,send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import ContactMessage
from twilio.rest import Client
from .models import Selling
from django.contrib.auth.decorators import login_required


from .models import user


# Create your views here.
# def show(request):
#     print('welcome')
#     return HttpResponse("MY PAGE")
def index(request):
    return render(request, 'index.html')
def contact(request):
    return render(request,'contact.html')
def properties(request):
    return render(request,'properties.html')
def services(request):
    return render(request,'services.html')
def about(request):
    return render(request,'about.html')
from .models import user

def signup(request):
    if request.method == 'POST':
        staff_id = request.POST.get('n1')
        username = request.POST.get('n2')
        password = request.POST.get('n3')
        phno = request.POST.get('n4')
        email = request.POST.get('n5')
        data = user.objects.filter(username=username)
        if list(data)==[]:
            d1=user.objects.create(staff_id=staff_id,username=username,password=password,phno=phno,email=email)
            d2=LoginData.objects.create(username=username,password=password)
            d1.save()
            d2.save()
            return render(request,'login.html')
        else:
            return HttpResponse('username already exists!')
    else:
        return render(request,'login.html')

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import LoginData

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import user  # your user model

def log(request):
    error_message = None  # store error

    if request.method == 'POST':
        r = request.POST.get('n2')  # username
        q = request.POST.get('n3')  # password

        # Admin login
        if r == 'admin' and q == '1234':
            request.session['a_id'] = r
            return redirect('admin_dashboard')

        # Normal user login
        try:
            d = user.objects.get(username=r)
            if d.password == q:
                request.session['u_id'] = r
                return redirect('user_dashboard')
            else:
                error_message = 'Incorrect password. Please try again.'
        except user.DoesNotExist:
            error_message = 'User not found. Please check your username.'

    return render(request, 'login.html', {'error_message': error_message})





from django.contrib.auth.decorators import login_required
from .models import UserPurchasedProperty, Payment, RefundRequest


from django.shortcuts import render, redirect
from .models import user, Payment, UserPurchasedProperty, RefundRequest

def user_dashboard(request):
    # ✅ check session
    if 'u_id' not in request.session:
        return redirect('log')  # Redirect if not logged in

    u = request.session['u_id']
    us = user.objects.get(username=u)

    # ✅ Update profile if form submitted
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')

        us.username = username
        us.email = email
        us.phone = phone

        if 'profile_picture' in request.FILES:
            us.profile_picture = request.FILES['profile_picture']

        us.save()
        messages.success(request, "Profile updated successfully!")
        return redirect('user_dashboard')  # Refresh page after save

    # ✅ Fetch all purchased properties of the user, latest first
    purchased_props = UserPurchasedProperty.objects.filter(user=us).order_by('-purchase_date')

    # ✅ Fetch all payments by the user
    payments = Payment.objects.filter(user=us).order_by('-created_at')

    # ✅ Fetch refund requests of the user
    refunds = RefundRequest.objects.filter(user=us).order_by('-created_at')

    context = {
        'user': us,
        'properties': purchased_props,
        'payments': payments,
        'refunds': refunds,
    }

    return render(request, 'profile.html', context)


from django.contrib import messages
from django.shortcuts import render, redirect
from .models import user

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect, get_object_or_404

def edit_property(request, id):
    p = get_object_or_404(Property, id=id)

    if request.method == "POST":
        p.title = request.POST.get("title")
        p.property_type = request.POST.get("property_type")
        p.location = request.POST.get("location")
        p.price = request.POST.get("price")
        p.bedrooms = request.POST.get("bedrooms")
        p.bathrooms = request.POST.get("bathrooms")
        p.description = request.POST.get("description")

        if "image" in request.FILES:
            p.image = request.FILES["image"]

        p.save()
        return redirect('admin_dashboard')

    return redirect('admin_dashboard')

def edit_profile(request):
    username = request.session.get('u_id')
    if not username:
        return redirect('log')

    us = user.objects.get(username=username)

    if request.method == 'POST':
        us.username = request.POST.get('username')
        password = request.POST.get('password')
        if password:
            us.password = make_password(password)  # Hash password before saving
        us.phone = request.POST.get('mobile')

        if 'profile_picture' in request.FILES:
            us.profile_picture = request.FILES['profile_picture']

        us.save()

        # Update session username
        request.session['u_id'] = us.username

        messages.success(request, "Profile Updated Successfully!")
        return redirect('user_dashboard')  # Redirect to dashboard after update

    # Render edit profile form on GET request
    return render(request, 'edit_profile.html', {'user': us})

def admin(request):
    if request.method == 'GET':
        data = user.objects.all()
        return render(request, 'admin_dashboard.html', {'property': data})
    return render(request, 'index.html')
def admin_properties(request):
    return render(request,'admin_properties.html')
def profile(request):
    if 'u_id' in request.session:
        return render(request, 'profile.html')
    elif 'a_id' in request.session:
        return render(request, 'admin_dashboard.html')
    else:
        return render(request,'index.html')


def change_password(request):
    if request.method == 'POST':
        o=request.POST['n1']
        p=request.POST['n2']
        q=request.POST['n3']
        data = login.objects.filter(password=o)
        data.update(password=p)
        if p !=q:
            return HttpResponse("password mismatch")
    return render(request,'passwordchange.html')


from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.conf import settings

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.conf import settings
from .models import PasswordReset
def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            u = user.objects.get(email=email)
        except:
            messages.info(request,"Email id not registered")
            return redirect(forgot_password)
        # Generate and save a unique token
        token = get_random_string(length=4)
        PasswordReset.objects.create(user=u, token=token)

        # Send email with reset link
        reset_link = reset_link = f'http://{request.get_host()}/reset/{token}'

        try:
            send_mail('Reset Your Password', f'Click the link to reset your password: {reset_link}','settings.EMAIL_HOST_USER', [email],fail_silently=False)
            # return render(request, 'emailsent.html')
        except:
            messages.info(request,"Network connection failed")
            return redirect(forgot_password)

    return render(request, 'forgot.html')



from django.contrib.auth.hashers import make_password
#reset password
def reset_password(request, token):
    # Verify token and reset the password
    password_reset = PasswordReset.objects.get(token=token)
    # usr = user.objects.get(id=password_reset.user_id)
    if request.method == 'POST':
        new_password = request.POST.get('newpassword')
        repeat_password = request.POST.get('cpassword')
        if repeat_password == new_password:
            u = password_reset.user.username
            log.objects.filter(username=u).update(password=new_password)

            # password_reset.user.password=new_password
            # password_reset.user.save()
            # # password_reset.delete()
            return redirect(log)
    return render(request, 'reset.html',{'token':token})


def register_form(request):
    if request.method=='POST':
        x = request.POST['p1']
        y = request.POST['p2']
        s = int(request.POST['p3'])
        u =request.POST['p4']
        v = request.POST['p5']
        w = request.POST['p6']
        z = user.objects.filter(username=v)
        t = user.objects.filter(email=u)
        if list(z) == []:
            if list(t) == []:
                data = user.objects.create(name=x, address=y, phno=s, email=u, username=v)
                data.save()
                data1 = login.objects.create(username=v, password=w, status=1)
                data1.save()
                return render(request, 'index.html')
            else:
                url = 'user.html'
                msg = '''<script>alert('email already exist')
                                    window.location='%s'</script>''' % (url)
                return HttpResponse(msg)
                return redirect(uregis)
        else:
            url = 'user.html'
            msg = '''<script>alert('username already exist')
                    window.location='%s'</script>''' % (url)
            return HttpResponse(msg)
            return redirect(uregis)

    else:
        return render(request,'usregister.html')


def properties_list(request):
    if request.method == 'GET':
        data = properties.objects.all()
        return render(request, 'admin_properties.html', {'r': data})
    return render(request, 'add_properties.html')

def admin_contact(request):
    return render(request,'admin_contact.html')




from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Property



def contact_agent(request):
    return render(request,'contact.html')

def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")

        # ✅ Save to database
        ContactMessage.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )

        # ✅ Send email to admin
        admin_message = f"""
        New contact form submission:

        Name: {name}
        Email: {email}
        Subject: {subject}

        Message:
        {message}
        """

        send_mail(
            subject=f"Contact Form: {subject}",
            message=admin_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=['your_admin_email@example.com'],  # change to your email
            fail_silently=False,
        )

        # ✅ HTML Auto-reply to user
        html_content = render_to_string('email_template.html', {
            'name': name,
            'subject': subject,
            'message': message,
        })
        text_content = strip_tags(html_content)

        email_message = EmailMultiAlternatives(
            subject="Thank you for contacting DreamNest Realty",
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[email],
        )
        email_message.attach_alternative(html_content, "text/html")
        email_message.send()

        messages.success(request, "✅ Your message has been sent! Check your email for confirmation.")
        return redirect('contact')

    return render(request, 'contact.html')

def email_templates(request):
    return render(request,'email_template.html')

from django.conf import settings

def send_sms(to_number, message):
    # Your Twilio credentials (keep them secret!)
    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN
    twilio_number = settings.TWILIO_PHONE_NUMBER

    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=message,
        from_=twilio_number,
        to=to_number
    )
    return message.sid
def Contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message_text = request.POST.get("message")

        # Send SMS
        send_sms(phone, f"Hi {name}, we received your message: {message_text}")

        messages.success(request, "Message sent via SMS!")
        return redirect('contact')

    return render(request, 'contact.html')


# views.py
from django.shortcuts import render, redirect
from .forms import SellingForm
from .models import Selling # Ensure the model is imported



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Property
from django.contrib.auth.hashers import make_password


# Admin Dashboard View
from .models import Property, User,Category

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Property, RefundRequest, Category  # assuming you have Category


# Add Property
from django.contrib.auth.models import User

# views.py

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .models import Property

def add_property(request):
    # ✅ Check session manually
    if 'u_id' not in request.session:
        return redirect('log')  # redirect to login page

    username = request.session['u_id']
    seller = user.objects.get(username=username)  # your custom user model

    if request.method == 'POST':
        title = request.POST.get('title')
        property_type = request.POST.get('property_type')
        location = request.POST.get('location')
        price = request.POST.get('price')
        bedrooms = request.POST.get('bedrooms')
        bathrooms = request.POST.get('bathrooms')

        image = request.FILES.get('image')  # ✅ Only one image

        # ✅ Create property and link to seller
        Property.objects.create(
            seller=seller,
            title=title,
            property_type=property_type,
            location=location,
            price=price,
            bedrooms=bedrooms,
            bathrooms=bathrooms,
            image=image,  # ✅ Single image saved correctly
            status='PENDING'  # ✅ Correct status based on your model choices
        )

        messages.success(request, "✅ Property added successfully! Pending admin approval.")
        return redirect('admin_dashboard')

    return redirect('admin_dashboard')

from django.shortcuts import render
from .models import Property

from django.db.models import Q

from itertools import chain
from django.shortcuts import render
from .models import Property, Selling  # ensure both models are imported

from itertools import chain
import datetime



from datetime import datetime
from django.shortcuts import render
from .models import Property, Selling # make sure Selling model is imported

from datetime import datetime
from django.shortcuts import render

from django.shortcuts import render
from .models import Property
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import datetime
from .models import Property, Category, RefundRequest
from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render
from .models import Property, Selling, RefundRequest, Category

from django.contrib.admin.views.decorators import staff_member_required
from .models import Selling


from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from .models import Selling, Property, User, RefundRequest, Category

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from .models import Property, user, RefundRequest, Selling, Category

from django.contrib.admin.views.decorators import staff_member_required


@staff_member_required
def admin_dashboard(request):
    properties = Property.objects.all().order_by('-id')
    users = user.objects.all().order_by('-id')
    refunds = RefundRequest.objects.all().order_by('-id')
    selling_requests = Selling.objects.filter(status='Pending').order_by('-id')
    categories = Category.objects.all()

    context = {
        'admin_username': request.user.username,
        'properties': properties,
        'users': users,
        'refunds': refunds,
        'selling_requests': selling_requests,
        'categories': categories,
    }
    return render(request, 'admin_dashboard.html', context)


from django.shortcuts import render
from .models import Property, RefundRequest
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from .models import Property, Payment, RefundRequest
from django.contrib import messages

def buy_properties(request):
    # Check session
    if 'u_id' not in request.session:
        return redirect('log')

    u = request.session['u_id']
    us = user.objects.get(username=u)

    # Fetch all properties (latest first)
    properties = Property.objects.all().order_by('-id')

    # Fetch all payments by this user
    user_payments = Payment.objects.filter(user=us).order_by('-created_at')

    # Fetch refund requests of this user
    refunds = RefundRequest.objects.filter(user=us).order_by('-created_at')

    # Fetch only this user's selling properties
    selling_properties = Selling.objects.filter(seller=us).order_by('-id')

    context = {
        'user': us,
        'properties': properties,
        'payments': user_payments,
        'refunds': refunds,
        'selling_properties': selling_properties,
    }

    return render(request, 'buy_properties.html', context)

from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Property

@login_required
def book_property(request, property_id):
    property_obj = get_object_or_404(Property, id=property_id)

    if not property_obj.is_active or property_obj.status in ['BOOKED', 'SOLD']:
        messages.warning(request, "Sorry, this property is no longer available.")
        return redirect('buy_properties')

    property_obj.buyer = request.user
    property_obj.status = 'BOOKED'
    property_obj.is_active = False
    property_obj.save()

    messages.success(request, "Property booked successfully!")
    return redirect('user_profile')

def delete_selling(request, id):
    """Delete a property from the Selling list."""
    if request.method == "POST":
        property_item = get_object_or_404(Selling, id=id)
        property_item.delete()
        messages.success(request, "❌ Property removed successfully!")
    return redirect('sell_listing')

def users(request):
    if request.method == 'GET':
        data = user.objects.all()
        return render(request, 'users.html', {'r': data})
    return render(request, 'index.html')


def delete_property(request, id):
    property_obj = get_object_or_404(Property, id=id)
    property_obj.delete()
    messages.success(request, "Property deleted successfully!")
    return redirect('admin_dashboard')  # change this to your dashboard view name



from django.shortcuts import render, get_object_or_404
from .models import Property, Selling
from django.shortcuts import render, get_object_or_404
from .models import Property, Selling, user  # Adjust imports as per your project

from django.shortcuts import render, get_object_or_404
from .models import Property, Selling, user  # Ensure 'user' is your custom model

def property_details(request, property_id):
    # Get the property object
    property_obj = get_object_or_404(Property, id=property_id)

    user_instance = None
    selling_properties = Selling.objects.none()  # default empty queryset

    if 'u_id' in request.session:
        try:
            username = request.session['u_id']
            user_instance = user.objects.get(username=username)
            # Fetch only this user's selling properties
            selling_properties = Selling.objects.filter(seller=user_instance).order_by('-id')
        except user.DoesNotExist:
            user_instance = None
            # selling_properties remains empty queryset

    context = {
        'property': property_obj,
        'user': user_instance,
        'selling_properties': selling_properties,
    }
    return render(request, 'property_details.html', context)

from django.shortcuts import render, get_object_or_404
from .models import Property

from django.shortcuts import render, get_object_or_404
from .models import Property
from django.shortcuts import render, get_object_or_404
from .models import Property


@login_required
def pay(request, property_id):
    property_obj = get_object_or_404(Property, id=property_id)

    if request.method == 'POST':
        amount_rupees = float(request.POST.get('amount', 0))  # User entered ₹1000
        amount_paise = int(amount_rupees * 100)  # Required by Razorpay (technical)

        context = {
            'property': property_obj,
            'amount_rupees': amount_rupees,  # display ₹1000
            'amount_paise': amount_paise,    # send 100000 (internal)
        }
        return render(request, 'pay.html', context)

    return render(request, 'payment.html', {'property': property_obj})


from .models import Payment
from .models import user, Payment, Property, UserPurchasedProperty
from django.shortcuts import render, redirect
from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from .models import user, Property, Payment, UserPurchasedProperty

def payment_success(request):
    payment_id = request.GET.get('payment_id')
    property_id = request.GET.get('property_id')
    amount = request.GET.get('amount')

    # ✅ Get custom user from session
    username = request.session.get('u_id')
    if not username:
        return redirect('log')

    try:
        us = user.objects.get(username=username)
    except user.DoesNotExist:
        return render(request, 'error.html', {'message': 'User not found in database!'})

    property_obj = get_object_or_404(Property, id=property_id)

    # ✅ Prevent double purchase
    if property_obj.status == 'SOLD':
        return render(request, 'success.html', {'message': 'This property is already sold.'})

    with transaction.atomic():
        # ✅ Create payment
        Payment.objects.create(
            user=us,
            property=property_obj,
            amount=amount,
            payment_id=payment_id,
            status='SUCCESS'
        )

        # ✅ Add to purchased table
        UserPurchasedProperty.objects.create(
            user=us,
            property=property_obj,
            amount_paid=amount,
            status='Purchased'
        )

        # ✅ Mark property sold to correct user instance
        property_obj.status = 'SOLD'
        property_obj.buyer = us  # <-- assign our custom user instance, not the class
        property_obj.save()

    return render(request, 'success.html', {
        'payment_id': payment_id,
        'amount': amount,
        'property': property_obj,
        'message': 'Payment Successful!',
    })
from django.shortcuts import redirect, render
from app.models import Payment, user  # your custom user model

def payment_history(request):
    username = request.session.get('u_id')
    if not username:
        return redirect('log')  # redirect to login if no session

    try:
        us = user.objects.get(username=username)
    except user.DoesNotExist:
        return render(request, 'error.html', {'message': 'User not found!'})

    payments = Payment.objects.filter(user=us).order_by('-created_at')
    return render(request, 'payment_history.html', {'payments': payments})




from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import UserPurchasedProperty, RefundRequest



from django.contrib.auth.decorators import login_required
from .models import UserPurchasedProperty, RefundRequest

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import UserPurchasedProperty, RefundRequest, user

def refund_request_submit(request):
    # Check session
    if 'u_id' not in request.session:
        return redirect('log')

    u = request.session['u_id']
    try:
        us = user.objects.get(username=u)
    except user.DoesNotExist:
        return render(request, 'error.html', {'message': 'User not found!'})

    if request.method == 'POST':
        purchase_id = request.POST.get('purchase_id')
        reason = request.POST.get('reason')

        # Get the purchased property
        purchased_property = get_object_or_404(UserPurchasedProperty, id=purchase_id, user=us)

        # Prevent duplicate refund requests
        if RefundRequest.objects.filter(purchased_property=purchased_property).exists():
            messages.warning(request, "Refund already requested for this property.")
            return redirect('user_dashboard')

        # ✅ Create new refund request and save the amount_paid
        RefundRequest.objects.create(
            user=us,
            purchased_property=purchased_property,
            reason=reason,
            amount_paid=purchased_property.amount_paid,  # save the paid amount
            status='Pending'
        )

        # Update property status
        purchased_property.status = 'Refund Requested'
        purchased_property.save()

        messages.success(request, "Refund request submitted successfully ✅")
        return redirect('user_dashboard')

    # If GET request, show a refund form
    purchased_properties = UserPurchasedProperty.objects.filter(user=us, status='Purchased')
    return render(request, 'refund_view.html', {'purchased_properties': purchased_properties})


from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import RefundRequest

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

def approve_refund(request, refund_id):
    # Get the refund request
    refund = get_object_or_404(RefundRequest, id=refund_id)
    purchased_property = refund.purchased_property
    user_obj = refund.user

    # Update refund status
    refund.status = 'Approved'
    refund.save()

    # Mark the purchased property as refunded
    purchased_property.status = 'Refunded'
    purchased_property.save()

    # Make the property available again
    prop = purchased_property.property
    prop.status = 'AVAILABLE'
    prop.sold = False
    prop.buyer = None
    prop.save()

    # Fetch amount from the refund record
    amount = refund.amount_paid

    if amount is None:
        # Send email alert to admin instead of user
        send_mail(
            subject='Refund Approved but Amount Missing ❗',
            message=f"Refund ID {refund.id} for user {user_obj.username} was approved, "
                    f"but the refunded amount is missing.",
            from_email=None,
            recipient_list=['admin@example.com'],
            fail_silently=False,
        )
        messages.warning(request, f"Refund approved, but amount missing! Admin notified.")

        # Optional: notify user anyway
        subject = 'Refund Approved ✅'
        message = f"""
Hello {user_obj.username},

Your refund request for the property '{prop.title}' has been approved by our team.

Property Details:
- Title: {prop.title}
- Location: {prop.location}
- Amount Refunded: To be processed
- Purchase Date: {purchased_property.purchase_date.strftime('%d %b %Y')}

The refunded amount will be processed to your original payment method shortly.

Thank you,
DreamNest Realty Team
"""
        send_mail(subject, message, None, [user_obj.email], fail_silently=False)

    else:
        # Send normal email to user
        subject = 'Refund Approved ✅'
        message = f"""
Hello {user_obj.username},

Your refund request for the property '{prop.title}' has been approved by our team.

Property Details:
- Title: {prop.title}
- Location: {prop.location}
- Amount Refunded: ₹{amount}
- Purchase Date: {purchased_property.purchase_date.strftime('%d %b %Y')}

The refunded amount will be processed to your original payment method shortly.

Thank you,
DreamNest Realty Team
"""
        send_mail(subject, message  , None, [user_obj.email], fail_silently=False)
        messages.success(request, f"Refund approved and email sent to {user_obj.email}")

    return redirect('admin_dashboard')

from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import datetime

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone

@login_required
def admin_approve_refund(request, refund_id):
    refund = get_object_or_404(RefundRequest, id=refund_id)
    refund.status = 'Approved'
    refund.admin_note = 'Your refund request has been approved.'  # optional admin note
    refund.updated_at = timezone.now()
    refund.save()

    # Update property and purchased record
    purchased_property = refund.purchased_property
    purchased_property.status = 'Refunded'
    purchased_property.save()

    property_obj = purchased_property.property

    # Send approval email
    subject = 'Refund Approved ✅'
    html_content = render_to_string('approve.html', {
        'user': refund.user,
        'property': property_obj,
        'purchased_property': purchased_property,
        'refund': refund,
        'site_url': request.build_absolute_uri('/'),
        'year': timezone.now().year,
    })
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, [refund.user.email])
    email.attach_alternative(html_content, "text/html")
    email.send()

    messages.success(request, f"Refund approved and email sent to {refund.user.email}")
    return redirect('admin_dashboard')


@login_required
def admin_reject_refund(request, refund_id):
    refund = get_object_or_404(RefundRequest, id=refund_id)
    refund.status = 'Rejected'
    refund.admin_note = 'Your refund request has been rejected.'  # optional admin note
    refund.updated_at = timezone.now()
    refund.save()

    purchased_property = refund.purchased_property
    purchased_property.status = 'Purchased'  # revert back
    purchased_property.save()

    property_obj = purchased_property.property

    # Send rejection email
    subject = 'Refund Rejected ❌'
    html_content = render_to_string('reject.html', {
        'user': refund.user,
        'property': property_obj,
        'purchased_property': purchased_property,
        'refund': refund,
        'site_url': request.build_absolute_uri('/'),
        'year': timezone.now().year,
    })
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, [refund.user.email])
    email.attach_alternative(html_content, "text/html")
    email.send()

    messages.warning(request, f"Refund rejected and email sent to {refund.user.email}")
    return redirect('admin_dashboard')



from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import RefundRequest

@receiver(post_save, sender=RefundRequest)
def update_property_on_refund(sender, instance, **kwargs):
    if instance.status == 'Approved':
        purchased_property = instance.purchased_property
        purchased_property.status = 'Refunded'
        purchased_property.save()

        prop = purchased_property.property
        prop.sold = False
        prop.save()

@login_required
def add_to_wishlist(request, property_id):
    property = get_object_or_404(Selling, id=property_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user, property=property)
    if created:
        # Optionally, show a message like "Added to wishlist"
        pass
    return redirect('view_wishlist')  # redirect back to property list

@login_required
def view_wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Selling
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from .models import Selling

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Selling, user  # Adjust if your user model is custom
from django.contrib.auth.decorators import login_required


@login_required
def selling_create(request):
    if request.method == 'POST':
        try:
            # ✅ Get user from session
            u = request.session.get('u_id')
            if not u:
                messages.error(request, "You must be logged in to submit a property.")
                return redirect('log')

            us = user.objects.get(username=u)  # Get actual user instance

            # ✅ Create Selling request
            Selling.objects.create(
                seller=us,  # proper user instance
                title=request.POST.get('title'),
                property_type=request.POST.get('property_type'),
                location=request.POST.get('location'),
                price=request.POST.get('price'),
                bedrooms=request.POST.get('bedrooms'),
                bathrooms=request.POST.get('bathrooms'),
                area=request.POST.get('area'),
                description=request.POST.get('description'),
                aadhaar_number=request.POST.get('aadhaar_number'),
                image=request.FILES.get('image'),
                status='Pending'
            )

            messages.success(request, "Your property selling request has been submitted!")
            return redirect('user_dashboard')

        except user.DoesNotExist:
            messages.error(request, "User not found. Please log in again.")
            return redirect('log')

        except Exception as e:
            messages.error(request, f"Error submitting property: {str(e)}")
            return redirect('sell_form')

    return render(request, 'sell_form.html')


from django.contrib.admin.views.decorators import staff_member_required

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from .models import Selling

from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def update_property_status(request, selling_id):
    if request.method == 'POST':
        action = request.POST.get('action')
        selling = get_object_or_404(Selling, id=selling_id)

        if action == 'approve':
            selling.status = 'Approved'
            selling.is_active = True  # Make it visible after approval
            messages.success(request, f"Property '{selling.title}' approved successfully!")
        elif action == 'reject':
            selling.status = 'Rejected'
            selling.is_active = False
            messages.warning(request, f"Property '{selling.title}' rejected.")

        selling.save()

    return redirect('admin_dashboard')
def practise(request):
    return render(request,'practise.html')