from django import forms
from .models import User
from django.contrib.auth.password_validation import validate_password


class UserRegistrationForm(forms.ModelForm):

    password = forms.CharField(required=True, validators=[validate_password],widget=forms.PasswordInput)
    password2 = forms.CharField(required=True,widget=forms.PasswordInput)
    birthdate = forms.DateField(
        widget=forms.SelectDateWidget
        )

    class Meta:
        model = User
        fields = ['email', 'first_name','last_name', 'birthdate','phone_number', 'password', 'password2']

    def clean(self):
        super(UserRegistrationForm, self).clean()

        # getting username and password from cleaned_data
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
    
        if password!= password2:
            raise forms.ValidationError({"password": "Password fields didn't match."})



    