from django.http import response
from django.test import TestCase
from django.contrib.auth import get_user_model


class TestSignUpView(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="ad@example.com",
            password="pass",
            username="abcd"
        )

    def test_get_success(self):
        '''
        「/recipe/siteUser/signup」へのGETリクエストをすると，
        ユーザ登録画面に遷移することを検証
        '''
        response = self.client.get('/recipe/siteUser/signup/')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].errors)
        self.assertTemplateUsed(response, 'recipe/siteUser/signup.html')

    def test_get_by_unauthenticated_user(self):
        '''
        ログイン済みのユーザーが GET リクエストすると，
        食材ランダム表示画面へリダイレクト
        '''
        # 上手くいかない...
        # redirect されていない
       
        logged_in = self.client.login(username=self.user.email, password="pass")
        self.assertTrue(logged_in)
        # self.client.force_login(self.user)
        response = self.client.get('/recipe/siteUser/signup/')
        self.assertRedirects(response, '/recipe/random')
        # self.assertTemplateUsed(response, 'recipe/random_recipe.html')

    def test_post_success(self):
        response = self.client.post('/recipe/siteUser/signup/', {
            'username': 'user',
            'email' : 'test@example.com',
            'password' : 'password',
            'password2' : 'password',
        })
        self.assertRedirects(response, '/recipe/random')
        self.assertTrue(get_user_model().objects.filter(username='user').exists())

    def test_with_same_username(self):
        response = self.client.post('/recipe/siteUser/signup/', {
            'username': 'abcdef',
            'email' : self.user.email,
            'password' : 'password',
            'password2' : 'password',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'email', 'そのメールアドレスは既に使われています')
        self.assertTemplateUsed(response, 'recipe/siteUser/signup.html')
        self.assertFalse(get_user_model().objects.filter(username='abcdef').exists())
