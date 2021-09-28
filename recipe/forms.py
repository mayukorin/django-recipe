from django import forms
from .models import SiteUser

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
            "username": forms.TextInput(attrs={"placeholder": "4文字以上で入力してください"}),
            "password": forms.PasswordInput(),
        }

    password2 = forms.CharField(
        label="確認用パスワード", required=True, widget=forms.PasswordInput(),
    )

    def clean_username(self):

        username = self.cleaned_data["username"]
        if len(username) < 4:
            raise forms.ValidationError("4文字以上で入力してください")

        return username

    def clean_email(self):
        email = self.cleaned_data["email"]
        return email

    def clean_password(self):
        password = self.cleaned_data["password"]
        return password

    def clean(self):

        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password != password2:
            raise forms.ValidationError("パスワードと確認用パスワードが一致しません")
        # ユニーク制約を自動でバリデーション
        super().clean()