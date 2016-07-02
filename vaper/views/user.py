# vim:sw=4 ts=4 et:
from django import forms
from django.contrib.auth.models import User
from django_quicky import routing, view
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404

url, urlpatterns = routing()

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
        ]

@url('^profile/$', name='user/profile')
@login_required
def profile(request):
    if request.method == 'POST':
        form = UserForm(request.POST, instance = request.user)
        if form.is_valid():
            form.save()
            form = UserForm(instance=request.user)
    else:
        form = UserForm(instance=request.user)

    return render(request, 'vaper/user/profile.html', {
            'user_form': form,
        })

class PasswordForm(forms.Form):
    curpass = forms.CharField(
        label='Current password',
        widget=forms.PasswordInput())

    newpass = forms.CharField(
        label='New password',
        widget=forms.PasswordInput())

    cnfpass = forms.CharField(
        label='Confirm new password',
        widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super(PasswordForm, self).clean()
        if cleaned_data.get('newpass') != cleaned_data.get('cnfpas'):
            raise forms.ValidationError("New passwords didn't match")

@url('^password/$', name='user/password')
@login_required
def password(request):
    form = PasswordForm()

    return render(request, 'vaper/user/password.html', {
            'password_form': form,
        })

class LoginForm(forms.Form):
    username = forms.CharField(max_length=64)
    password = forms.CharField(max_length=64, widget=forms.PasswordInput())

@url('^login/$', name='user/login')
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                    username = form.cleaned_data['username'],
                    password = form.cleaned_data['password'])
            if user is not None and user.is_active:
                login(request, user)
                return redirect('vaper:index')
            else:
                form.add_error('password', 'Invalid password')
    else:
        form = LoginForm()

    return render(request, 'vaper/user/login.html', {
        'form': form,
    })
