from django.conf import settings
from django.core.mail import BadHeaderError, EmailMessage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import ContactForm

def contact(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = "Website Inquiry From Amlaw Design"
            name = form.cleaned_data['name']
            namemessage = 'From: ' + name
            email = form.cleaned_data['email']
            emailmessage = 'Email: ' + email
            phone = form.cleaned_data['phone']
            website = form.cleaned_data['website']
            preferred = form.cleaned_data['preferred']

            if preferred == 'Phone':
                pref = 'Preferred method of contact is phone.'
            elif preferred == 'Text':
                pref = 'Preferred method of contact is text.'
            else:
                pref = 'Preferred method of contact is email.'

            if phone:
                phone_num = 'Phone number: ' + phone
            else:
                phone_num = 'No phone number given.'

            body = {'namemessage': namemessage, 'emailmessage': emailmessage, 'phone_num':phone_num, 'pref':pref, 'message':form.cleaned_data['message'],
                    'website':website}
            message = "\n".join(body.values())

            try:
                email_msg = EmailMessage(subject, message, settings.EMAIL_HOST_USER,
                                         [settings.EMAIL_HOST_USER], reply_to=[email])
                email_msg.send()
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('success/')
    return render(request, 'contact/contact.html', {'form': form})

def success(request):
    return render(request, 'contact/success.html')
