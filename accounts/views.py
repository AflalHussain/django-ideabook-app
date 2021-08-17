from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, UserProfileForm
from .models import UserProfile



# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            profile=UserProfile(profile_user=user)
            profile.profile_pic='images/user-default.png'
            profile.save()
            return redirect('setup_profile')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})
@login_required
def setup_profile(request):
    profile=UserProfile.objects.get(profile_user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES,instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.save()
            return redirect('feed')
    else:
        form = UserProfileForm()
    return render(request, 'accounts/setup_profile.html', {'form': form})