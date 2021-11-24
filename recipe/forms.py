from django import forms
from .models import SiteUser
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm


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
                "required": "ユーザ名を入力してください",
                "max_length": "名前は150字以内で入力してください",
            },
            "password": {"required": "パスワードを入力してください"},
            "email": {
                "required": "メールアドレスを入力してください",
                "unique": "そのメールアドレスは既に使われています",
                "invalid": "メールアドレスは正しい形式で入力してください",
            },
        }

    password2 = forms.CharField(
        label="確認用パスワード",
        required=True,
        error_messages={"required": "確認用パスワードを入力してください"},
        widget=forms.PasswordInput(),
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
                "required": "ユーザ名を入力してください",
                "max_length": "名前は150字以内で入力してください",
            },
            "email": {
                "required": "メールアドレスを入力してください",
                "unique": "そのメールアドレスは既に使われています",
                "invalid": "メールアドレスは正しい形式で入力してください",
            },
        }


class PasswordEditForm(PasswordChangeForm):

    new_password1 = forms.CharField(
        label="新しいパスワード",
        # strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
        error_messages={"required": "新しいパスワードを入力してください",},
    )

    new_password2 = forms.CharField(
        label="確認用パスワード",
        # strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
        error_messages={"required": "確認用パスワードを入力してください",},
    )

    old_password = forms.CharField(
        label="現在のパスワード",
        # strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
        error_messages={"required": "現在のパスワードを入力してください",},
    )

    error_messages = {
        "password_mismatch": "新しいパスワードと確認用パスワードが一致しません",
        "password_incorrect": "現在のパスワードが正しくありません",
    }


class SignInForm(AuthenticationForm):

    username = forms.EmailField(
        widget=forms.TextInput(attrs={"autofocus": True}),
        error_messages={
            "required": "メールアドレスを入力してください",
            "invalid": "メールアドレスは正しい形式で入力してください",
        },
    )
    
    password = forms.CharField(
        label="パスワード",
        # strip=False,
        required=True,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
        error_messages={"required": "パスワードを入力してください",},
    )
    error_messages = {
        "invalid_login": "メールアドレスかパスワードが間違っています",
        "inactive": "アカウントが有効ではありません",
    }
    
    
    