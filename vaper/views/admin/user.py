# vim:sw=4 ts=4 et:

from django_quicky import routing, view
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django import forms
from vaper.decorators import superuser_required

url, urlpatterns = routing()

@url('^list/', name='admin/user/list')
@superuser_required
def list(request):
    users = User.objects.all().order_by('username')
    return render(request, 'vaper/admin/user/list.html', {
        'users': users,
    })

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
        ]

@url('^edit/(?P<id>[0-9]+)/$', name='admin/user/edit')
@superuser_required
def edit(request, id):
    user = get_object_or_404(User, id=id)

    if request.method == 'POST':
        form = UserForm(request.POST, instance = user)
        if form.is_valid():
            form.save()
            form = UserForm(instance=user)
    else:
        form = UserForm(instance=user)

    return render(request, 'vaper/admin/user/edit.html', {
            'form': form,
        })

class PasswordForm(forms.Form):
    newpass = forms.CharField(
        label='New password',
        widget=forms.PasswordInput())

    cnfpass = forms.CharField(
        label='Confirm new password',
        widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super(PasswordForm, self).clean()
        if cleaned_data.get('newpass') != cleaned_data.get('cnfpass'):
            raise forms.ValidationError({ 'cnfpass': "New passwords didn't match" })

@url('^password/(?P<id>[0-9]+)/$', name='admin/user/password')
@superuser_required
def password(request, id):
    user = get_object_or_404(User, id=id)

    if request.method == 'POST':
        form = PasswordForm(request.POST)
        if form.is_valid():
            user.password = form.cleaned_data['newpass']
            return redirect('vaper:admin/user/edit', id=user.id)
    else:
        form = PasswordForm()

    return render(request, 'vaper/admin/user/password.html', {
            'form': form,
            'instance': user,
        })
