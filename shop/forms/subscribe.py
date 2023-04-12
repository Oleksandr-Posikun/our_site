from django import forms


class LoginForm(forms.Form):
    login_email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Enter Your Email'})
    )
    login_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter Your Password'})
    )
    login_remember = forms.BooleanField(
        initial=True,
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'defult-check'})
    )


class RegistrationForm(forms.Form):
    registration_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Enter Your name'})
    )
    registration_email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Enter Your Email'})
    )
    registration_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter Your Password'})
    )
    registration_confirm_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirmation Password'})
    )
    registration_accept_terms = forms.BooleanField(
        initial=True,
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'defult-check'})
    )