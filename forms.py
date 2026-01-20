from django import forms
from .models import Selling
from django import forms
from .models import ContactAgent

class ContactAgentForm(forms.ModelForm):
    class Meta:
        model = ContactAgent
        fields = ['name', 'email', 'phone', 'message']

class SellingForm(forms.ModelForm):
    class Meta:
        model = Selling
        fields = '__all__'
from django import forms
from .models import Property

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = [
            'title', 'location', 'price', 'bedrooms', 'bathrooms', 'image',
            'category', 'property_type', 'status', 'is_active'
        ]
