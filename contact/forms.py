from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': ''}), required=True)
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': ''}), required=True)
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': ''}), required=False)
    CHOICES = (('Email', 'Email'),('Phone', 'Phone'),('Text', 'Text'),)
    preferred = forms.ChoiceField(widget=forms.Select(attrs={'class': ''}), choices=CHOICES)
    website = forms.CharField(widget=forms.TextInput(attrs={'class': '', 'placeholder': 'www.yourwebsite.com'}),
                              required=False)
    message = forms.CharField(widget=forms.Textarea(attrs={'class': ''}), required=True)
