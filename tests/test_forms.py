from django.contrib.auth.models import User
from django.test import TestCase
from recipe.forms import SignUpForm, UserPropertyChangeForm, PasswordEditForm, SignInForm
from recipe.models import SiteUser
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password

class TestSignUpForm(TestCase):

    @classmethod
    def setUpTestData(cls):
        get_user_model().objects.create_user(
            email='same@example.com',
            password='pass',
            username='aaa',
        )

    def test_success(self):
        input_data = {
            'username' : 'abcd',
            'email' : 'abcd@example.com',
            'password' : 'password',
            'password2' : 'password',
        }
        form = SignUpForm(input_data)
        self.assertTrue(form.is_valid())

    def test_with_username_blank(self):
        input_data = {
            'username' : ' ',
            'email' : 'abcd@example.com',
            'password' : 'password',
            'password2' : 'password2',
        }
        form = SignUpForm(input_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['username'], ['ユーザ名を入力してください'])

    def test_with_email_blank(self):
        input_data = {
            'username' : 'abc',
            'email' : ' ',
            'password' : 'password',
            'password2' : 'password2',
        }
        form = SignUpForm(input_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['email'], ['メールアドレスを入力してください'])

    def test_with_password_blank(self):
        input_data = {
            'username' : 'abc',
            'email' : 'abcd@example.com',
            'password' : ' ',
            'password2' : 'password2',
        }
        form = SignUpForm(input_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['password'], ['パスワードを入力してください'])

    def test_with_password2_blank(self):
        input_data = {
            'username' : 'abc',
            'email' : 'abcd@example.com',
            'password' : 'abcccc',
            'password2' : ' ',
        }
        form = SignUpForm(input_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['password2'], ['確認用パスワードを入力してください'])

    def test_with_not_same_password(self):
        input_data = {
            'username' : 'abcd',
            'email' : 'abcd@example.com',
            'password' : 'password',
            'password2' : 'password2',
        }
        form = SignUpForm(input_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.non_field_errors(), ['パスワードと確認用パスワードが一致しません'])

    def test_with_long_username(self):
        long_user_name = ""
        for _ in range(200):
            long_user_name += "a"

        input_data = {
            'username' : long_user_name,
            'email' : 'abcd@example.com',
            'password' : 'password',
            'password2' : 'password',
        }
        form = SignUpForm(input_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['username'], ['名前は150字以内で入力してください'])

    def test_with_invalid_email(self):
        input_data = {
            'username' : 'abcd',
            'email' : 'abcd',
            'password' : 'password',
            'password2' : 'password',
        }
        form = SignUpForm(input_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['email'], ['メールアドレスは正しい形式で入力してください'])

    def test_with_duplicate_email(self):
        input_data = {
            'username' : 'abcd',
            'email' : 'same@example.com',
            'password' : 'password',
            'password2' : 'password',
        }
        form = SignUpForm(input_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['email'], ['そのメールアドレスは既に使われています'])


class TestUserPropertyChangeForm(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            email='same@example.com',
            password='pass',
            username='aaa',
        )
        get_user_model().objects.create_user(
            email='same2@example.com',
            password='pass',
            username='aaa',
        )

    def test_post_success(self):

        input_data = {
            'username' : 'abcd',
            'email' : 's@example.com',
        }
        form = UserPropertyChangeForm(input_data, instance=self.user)
        self.assertTrue(form.is_valid())
        self.assertEqual(self.user.username, 'abcd')
        self.assertEqual(self.user.email, 's@example.com')

    def test_with_username_blank(self):

        input_data = {
            'username' : ' ',
            'email' : 's@example.com',
        }
        form = UserPropertyChangeForm(input_data, instance=self.user)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['username'], ['ユーザ名を入力してください'])

    def test_with_email_blank(self):

        input_data = {
            'username' : 'abcd',
            'email' : ' ',
        }
        form = UserPropertyChangeForm(input_data, instance=self.user)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['email'], ['メールアドレスを入力してください'])


    def test_with_long_username(self):

        long_user_name = ""
        for _ in range(200):
            long_user_name += "a"

        input_data = {
            'username' : long_user_name,
            'email' : 's@example.com',
        }
        form = UserPropertyChangeForm(input_data, instance=self.user)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['username'], ['名前は150字以内で入力してください'])

    def test_with_invalid_email(self):
        input_data = {
            'username' : 'abcd',
            'email' : 's',
        }
        form = UserPropertyChangeForm(input_data, instance=self.user)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['email'], ['メールアドレスは正しい形式で入力してください'])

    def test_success_only_username_change(self):
        input_data = {
            'username' : 'abcd',
            'email' : 'same@example.com',
        }
        form = UserPropertyChangeForm(input_data, instance=self.user)
        self.assertTrue(form.is_valid())
        self.assertEqual(self.user.username, 'abcd')
        self.assertEqual(self.user.email, 'same@example.com')

    def test_with_duplicate_email(self):
        input_data = {
            'username' : 'abcd',
            'email' : 'same2@example.com',
        }
        form = UserPropertyChangeForm(input_data, instance=self.user)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['email'], ['そのメールアドレスは既に使われています'])
    


class TestSignInForm(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            email='same@example.com',
            password='pass',
            username='aaa',
        )

    def test_post_success(self):
        input_data = {
            'username': 'same@example.com',
            'password': 'pass'
        }
        form = SignInForm(data=input_data)
        self.assertTrue(form.is_valid())

    
    def test_with_password_blank(self):
        input_data = {
            'username': 'same@example.com',
            'password': ' '
        }
        form = SignInForm(data=input_data)
        self.assertFalse(form.is_valid())
        # self.assertEqual(form.non_field_errors(), ['メールアドレスかパスワードが間違っています'])
        self.assertEqual(form.errors['password'], ['パスワードを入力してください'])
    
    def test_with_username_blank(self):
        input_data = {
            'username': ' ',
            'password': 'pass'
        }
        form = SignInForm(data=input_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['username'], ['メールアドレスを入力してください'])

    def test_with_invalid_username_blank(self):
        input_data = {
            'username': 'same',
            'password': 'pass'
        }
        form = SignInForm(data=input_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['username'], ['メールアドレスは正しい形式で入力してください'])


    def test_with_wrong_password(self):
        input_data = {
            'username': 'same@example.com',
            'password': 'pas'
        }
        form = SignInForm(data=input_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.non_field_errors(), ['メールアドレスかパスワードが間違っています'])

   
    


class TestPasswordEditForm(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            email='same@example.com',
            password='pass',
            username='aaa',
        )

    def test_post_success(self):
        input_data = {
            'new_password1' : 'newpass',
            'new_password2' : 'newpass',
            'old_password' : 'pass'
        }
        form = PasswordEditForm(self.user, input_data)
        self.assertTrue(form.is_valid())
        self.assertTrue(check_password('pass', SiteUser.objects.get(id=self.user.id).password))


    def test_with_new_password_1_blank(self):
        input_data = {
            'new_password1' : ' ',
            'new_password2' : 'newpass',
            'old_password' : 'pass'
        }
        form = PasswordEditForm(self.user, input_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['new_password1'], ['新しいパスワードを入力してください'])

    def test_with_new_password_2_blank(self):
        input_data = {
            'new_password1' : 'newpass',
            'new_password2' : ' ',
            'old_password' : 'pass'
        }
        form = PasswordEditForm(self.user, input_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['new_password2'], ['確認用パスワードを入力してください'])

    def test_with_old_password_blank(self):
        input_data = {
            'new_password1' : 'newpass',
            'new_password2' : 'newpass',
            'old_password' : ' '
        }
        form = PasswordEditForm(self.user, input_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['old_password'], ['現在のパスワードを入力してください'])

    def test_with_not_same_password(self):
        input_data = {
            'new_password1' : 'newpass',
            'new_password2' : 'newpasss',
            'old_password' : 'pass'
        }
        form = PasswordEditForm(self.user, input_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['new_password2'], ['新しいパスワードと確認用パスワードが一致しません'])

    def test_with_wrong_old_password(self):
        input_data = {
            'new_password1' : 'newpass',
            'new_password2' : 'newpass',
            'old_password' : 'passs'
        }
        form = PasswordEditForm(self.user, input_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['old_password'], ['現在のパスワードが正しくありません'])
        
