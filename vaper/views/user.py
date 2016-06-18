# vim:sw=4 ts=4 et:
from django import forms
from django.contrib.auth.models import User
from django_quicky import routing, view
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

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
