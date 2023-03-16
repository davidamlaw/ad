from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from . import forms
from .models import Profile
from django.http import HttpResponseRedirect

class SignUp(CreateView):
    form_class = forms.SignUpForm
    success_url = '/accounts/login/'
    template_name = 'accounts/signup.html'

    def form_invalid(self, form, **kwargs):
        ctx = self.get_context_data(**kwargs)
        ctx['form'] = form
        return self.render_to_response(ctx)

    def form_valid(self, form):
    	form.save()
    	username = self.request.POST['email']
    	password = self.request.POST['password1']
    	user = authenticate(username=username, password=password)
    	login(self.request, user)
    	return HttpResponseRedirect('/accounts/profile/')

@login_required
def profile(request):
    return render(request, 'accounts/profile.html')

@login_required
def edit_profile(request):
    if request.method == 'POST':
        user = request.user
        try:
        	profile_pic = request.FILES['profile_pic']
        except:
        	profile_pic = False
        try:
        	profile = Profile.objects.get(user=user)
        except:
        	profile = False
        if profile:
            if profile_pic:
                profile.profile_pic = profile_pic
            profile.title = request.POST.get('title')
            profile.bio = request.POST.get('bio')
            profile.save()
        else:
            profile = Profile(user=user)
            if profile_pic:
            	profile.profile_pic = profile_pic
            profile.title = request.POST.get('title')
            profile.bio = request.POST.get('bio')
            profile.save()
        return redirect('/accounts/profile/')
    return render(request, 'accounts/edit_profile.html')
