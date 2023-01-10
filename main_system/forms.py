from django import forms
from .models import Account, Tranfer, Borrower, Lender, applyLoan, Verificaton
from django.contrib.auth.forms import UserCreationForm, User, UserChangeForm, PasswordChangeForm


class TransferForm(forms.ModelForm):
    class Meta:
        model = Tranfer
        fields = ('recieving_user','amount' )
        widgets = {
            'recieving_user': forms.TextInput(attrs={'class': 'form-control'}),
            'amount': forms.TextInput(attrs={'class': 'form-control'}),


        }


class VerificationForm(forms.ModelForm):
    class Meta:
        model = Verificaton
        fields = ('document','Level' )
        widgets = {
            'document': forms.TextInput(attrs={'class': 'form-control'}),
            'Level': forms.Select(attrs={'class': 'form-control'}),


        }

class ApplyForm(forms.ModelForm):
    class Meta:
        model = applyLoan
        fields = ('comment','file_1','file_2','file_3' )

        widgets = {
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': '5'}),
        }



class BorrowersForm(forms.ModelForm):
    class Meta:
        model = Borrower
        fields = ('amount','percentage', 'duration', 'purpose',)

        widgets = {
            'amount': forms.TextInput(attrs={'class': 'form-control'}),
            'purpose': forms.Textarea(attrs={'class': 'form-control', 'rows': '7'}),
            'percentage': forms.TextInput(attrs={'class': 'custom-select'}),
            'duration': forms.TextInput(attrs={'class': 'custom-select'}),
        }


class LenderForm(forms.ModelForm):
    class Meta:
        model = Lender
        fields = ('amount','percentage', 'duration', 'conditions',)

        widgets = {
            'amount': forms.TextInput(attrs={'class': 'form-control'}),
            'conditions': forms.Textarea(attrs={'class': 'form-control', 'rows': '7'}),
            'percentage': forms.TextInput(attrs={'class': 'custom-select'}),
            'duration': forms.TextInput(attrs={'class': 'custom-select'}),
        }


class LenderUpdateForm(forms.ModelForm):
    class Meta:
        model = Lender
        fields = ('Lender_approval','amount','percentage', 'duration', 'conditions',)

        widgets = {
            'amount': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'conditions': forms.Textarea(attrs={'class': 'form-control', 'rows': '7', 'readonly': 'readonly'}),
            'percentage': forms.TextInput(attrs={'class': 'custom-select', 'readonly': 'readonly'}),
            'duration': forms.TextInput(attrs={'class': 'custom-select', 'readonly': 'readonly'}),
        }


class SignupForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['type'] = 'password'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['type'] = 'password'