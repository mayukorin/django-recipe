from django.test import TestCase
from recipe.forms import SignUpForm

class TestSignUpForm(TestCase):

    def test_post_success(self):
        input_data = {
            'username' : 'abcd',
            'email' : 'abcd@example.com',
            'password' : 'password',
            'password2' : 'password',
        }
        form = SignUpForm(input_data)
        self.assertTrue(form.is_valid())
