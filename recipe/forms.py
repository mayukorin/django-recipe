from django import forms
from .models import SiteUser
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.core.exceptions import ValidationError

class SiteUserRegisterForm(forms.ModelForm):
    class Meta:
        model = SiteUser

        fields = (
            "username",
            "email",
            "password",
        )

        labels = {
            "password": "パスワード",
        }

        widgets = {
            "username": forms.TextInput(),
            "password": forms.PasswordInput(),
        }

        error_messages = {
            "username": {
                "required" : "ユーザ名を入力してください",
                "max_length" : "名前は150字以内で入力してください"
            },
            "password": {
                "required" : "パスワードを入力してください"
            },
            "email" : {
                "required" : "メールアドレスを入力してください",
                "unique" : "そのメールアドレスは既に使われています",                                  
                "invalid" : "メールアドレスは正しい形式で入力してください"
            }
        }

    password2 = forms.CharField(
        label="確認用パスワード", required=True, error_messages={'required': '確認用パスワードを入力してください'}, widget=forms.PasswordInput(),
    )


    def clean(self):

        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password != password2:
            raise forms.ValidationError("パスワードと確認用パスワードが一致しません")
        # ユニーク制約を自動でバリデーション
        super().clean()

class SignUpForm(forms.ModelForm):
    class Meta:
        model = SiteUser

        fields = (
            "username",
            "email",
            "password",
        )

        labels = {
            "password": "パスワード",
        }

        widgets = {
            "username": forms.TextInput(),
            "password": forms.PasswordInput(),
        }

        error_messages = {
            "username": {
                "required" : "ユーザ名を入力してください",
                "max_length" : "名前は150字以内で入力してください"
            },
            "password": {
                "required" : "パスワードを入力してください"
            },
            "email" : {
                "required" : "メールアドレスを入力してください",
                "unique" : "そのメールアドレスは既に使われています",                                  
                "invalid" : "メールアドレスは正しい形式で入力してください"
            }
        }

    password2 = forms.CharField(
        label="確認用パスワード", required=True, error_messages={'required': '確認用パスワードを入力してください'}, widget=forms.PasswordInput(),
    )


    def clean(self):

        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password != password2:
            raise forms.ValidationError("パスワードと確認用パスワードが一致しません")
        # ユニーク制約を自動でバリデーション
        super().clean()


class UserPropertyChangeForm(forms.ModelForm):
    class Meta:
        model = SiteUser

        fields = (
            "username",
            "email",
        )


        widgets = {
            "username": forms.TextInput(),
        }

        error_messages = {
            "username": {
                "required" : "ユーザ名を入力してください",
                "max_length" : "名前は150字以内で入力してください"
            },
            "email" : {
                "required" : "メールアドレスを入力してください",
                "unique" : "そのメールアドレスは既に使われています",                                  
                "invalid" : "メールアドレスは正しい形式で入力してください"
            }
        }

class PasswordEditForm(PasswordChangeForm):

    
    new_password1 = forms.CharField(
        label= '新しいパスワード',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
        error_messages={
            'required' : '新しいパスワードを入力してください',
        }
    )

    new_password2 = forms.CharField(
        label= '確認用パスワード',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
        error_messages={
            'required' : '確認用パスワードを入力してください',
        }
    )

    old_password = forms.CharField(
        label= '現在のパスワード',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
        error_messages={
            'required' : '現在のパスワードを入力してください',
        }
    )

    error_messages = {
        'password_mismatch' : '新しいパスワードと確認用パスワードが一致しません',
        'password_incorrect': '現在のパスワードが正しくありません',
    } 

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        return password2

    def clean_old_password(self):
        """
        Validate that the old_password field is correct.
        """
        old_password = self.cleaned_data["old_password"]
        print(old_password)
        print(self.user.check_password(old_password))
        print("----")
        if not self.user.check_password(old_password):
            raise ValidationError(
                self.error_messages['password_incorrect'],
                code='password_incorrect',
            )
        return old_password



class SiteUserLoginForm(forms.Form):

    email = forms.EmailField(label="メールアドレス", 
                            error_messages={
                                'required': 'メールアドレスを入力してください',
                                "invalid" : "メールアドレスは正しい形式で入力してください"
                            })
    password = forms.CharField(
        label="パスワード", widget=forms.PasswordInput(),
        error_messages={
            "required" : "パスワードを入力してください"
        }
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.site_user_cache = None

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        try:
            site_user = SiteUser.objects.get(email=email)
        except ObjectDoesNotExist:
            raise forms.ValidationError("メールアドレスかパスワードが間違っています")
        if not site_user.check_password(password):
            raise forms.ValidationError("メールアドレスかパスワードが間違っています")

        self.site_user_cache = site_user

    def get_site_user(self):
        return self.site_user_cache


class SignInForm(AuthenticationForm):

    username = forms.EmailField(
        widget=forms.TextInput(attrs={'autofocus': True}),
        error_messages={
            'required': 'メールアドレスを入力してください',
            'invalid' : 'メールアドレスは正しい形式で入力してください'
        }
        
    )

    password = forms.CharField(
        label= 'パスワード',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
        error_messages={
            'required' : 'パスワードを入力してください',
        }
    )

    error_messages = {
        'invalid_login' : 'メールアドレスかパスワードが間違っています',
        'inactive' : 'アカウントが有効ではありません',
    }

