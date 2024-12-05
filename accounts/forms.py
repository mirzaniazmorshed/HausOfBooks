from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .constants import GENDER,ACCOUNT_TYPE
from .models import UserAccountModel,UserAddressModel
class UserSignUpForm(UserCreationForm):
    gender = forms.ChoiceField(choices=GENDER)
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    account_type = forms.ChoiceField(choices=ACCOUNT_TYPE)

    street_address = forms.CharField(max_length=100)
    city = forms.CharField(max_length=100)
    postal_code = forms.IntegerField()
    country = forms.CharField(max_length=100)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'gender', 'birth_date', 'street_address', 'city', 'postal_code', 'country', 'email']

    
    def save(self, commit=True):
        user_obj = super().save(commit=False)
        if commit == True:
            user_obj.save()
            gender = self.cleaned_data.get('gender')
            birth_date = self.cleaned_data.get('birth_date')
            account_type = self.cleaned_data.get('account_type')


            street_address = self.cleaned_data.get('street_address')
            city = self.cleaned_data.get('city')
            postal_code = self.cleaned_data.get('postal_code')
            country = self.cleaned_data.get('country')

            UserAccountModel.objects.create(
                user = user_obj,
                birth_date = birth_date,
                gender = gender,
                account_no = 1000+user_obj.id,
                account_type = account_type
            )
            UserAddressModel.objects.create(
                user = user_obj,
                street_address = street_address,
                postal_code = postal_code,
                city =city,
                country = country
            )

class UserDepositForm(forms.Form):
    deposit_amount = forms.IntegerField(required=True)
    
    def clean_deposit_amount(self):
        amount = self.cleaned_data.get('deposit_amount')
        if amount < 1000:
            raise forms.ValidationError("The minimum deposit amount is $1000.")
        return amount
    