from django import forms
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

from oldmail.models import Account, Profile


class AccountChangeForm(forms.ModelForm):
    name = forms.CharField()

    class Meta:
        model = Account

        fields = (
            'name',
        )

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name:
            try:
                Account.objects.get(slug=slugify(name))
                self._errors['name'] = ['That account name is already taken. Please pick a new one.']
            except:
                pass
        return name

    def save_account(self):
        # Save the Account with the new name and slug
        a = self.instance
        a.name = self.cleaned_data['name']
        a.slug = slugify(self.cleaned_data['name'])
        a.save()
        return a


class AccountAddForm(forms.ModelForm):
    account = forms.CharField()
    email = forms.CharField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput(render_value=False))

    class Meta:
        model = User

        fields = (
            'account',
            'first_name',
            'last_name',
            'email',
            'password',
        )

    def clean_account(self):
        account = self.cleaned_data.get('account')
        if account:
            try:
                Account.objects.get(slug=slugify(account))
                self._errors['account'] = ['That account name is already taken. Please pick a new one.']
            except:
                pass
        return account

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            try:
                User.objects.get(username=email)
                self._errors['email'] = ['That email is already taken. Do you already have an account?']
            except:
                pass
        return email

    def add_account(self):
        # Add the initial Account
        a = Account.objects.create(name=self.cleaned_data['account'], slug=slugify(self.cleaned_data['account']))
        return a

    def add_profile(self, account):
        # Add the profile
        u = User.objects.create(first_name=self.cleaned_data['first_name'],
                                last_name=self.cleaned_data['last_name'],
                                email=self.cleaned_data['email'],
                                username=self.cleaned_data['email'])
        u.set_password(self.cleaned_data['password'])
        u.save()
        p = Profile.objects.create(user=u, account=account, is_account_admin=True)
        # TODO send password_reset confirmation
        return p
