from django import forms

class CreateNewUser(forms.Form):
    username = forms.CharField(label="Username", max_length=200)
    fname = forms.CharField(label="First Name", max_length=200)
    lname = forms.CharField(label="Last Name", max_length=200)
    email = forms.EmailField(label="Email",required=True)
    pass1 = forms.CharField(label="Password",widget=forms.PasswordInput())
    pass2 = forms.CharField(label="Confirm password",widget=forms.PasswordInput())

class SignInForm(forms.Form):
    username = forms.CharField(label="Username", max_length=200)
    pass1 = forms.CharField(label="Password",widget=forms.PasswordInput())
