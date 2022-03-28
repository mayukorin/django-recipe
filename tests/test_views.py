from django.http import response
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password

class TestSignUpView(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="ad@example.com",
            password="pass",
            username="abcd"
        )

    def test_get_success(self):
        '''
        「/recipe/site_user/signup」へのGETリクエストをすると，
        ユーザ登録画面に遷移することを検証
        '''
        response = self.client.get('/recipe/site_user/signup/')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].errors)
        self.assertTemplateUsed(response, 'recipe/site_user/signup.html')

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
        response = self.client.get('/recipe/site_user/signup/')
        self.assertRedirects(response, '/recipe/recipes/random')
        # self.assertTemplateUsed(response, 'recipe/recipes/random_recipe.html')

    def test_post_success(self):
        response = self.client.post('/recipe/site_user/signup/', {
            'username': 'user',
            'email' : 'test@example.com',
            'password' : 'password',
            'password2' : 'password',
        })
        self.assertRedirects(response, '/recipe/recipes/random')
        self.assertTrue(get_user_model().objects.filter(username='user').exists())

    def test_with_same_username(self):
        response = self.client.post('/recipe/site_user/signup/', {
            'username': 'abcdef',
            'email' : self.user.email,
            'password' : 'password',
            'password2' : 'password',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'email', 'そのメールアドレスは既に使われています')
        self.assertTemplateUsed(response, 'recipe/site_user/signup.html')
        self.assertFalse(get_user_model().objects.filter(username='abcdef').exists())



class TestSignInView(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="ad@example.com",
            password="pass",
            username="abcd"
        )

    def test_get_success(self):
        '''
        「/recipe/site_user/signin」へのGETリクエストをすると，
        ログイン登録画面に遷移することを検証
        '''
        response = self.client.get('/recipe/site_user/signin/')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].errors)
        self.assertTemplateUsed(response, 'recipe/site_user/signin.html')

    def test_get_by_authenticated_user(self):
        '''
        ログイン済みのユーザーが GET リクエストすると，
        食材ランダム表示画面へリダイレクト
        '''
       
        logged_in = self.client.login(username=self.user.email, password="pass")
        self.assertTrue(logged_in)
        response = self.client.get('/recipe/site_user/signin/')
        self.assertRedirects(response, '/recipe/recipes/random')

    def test_post_success(self):
        response = self.client.post('/recipe/site_user/signin/', {
            'username': 'ad@example.com',
            'password' : 'pass',
        })
        self.assertRedirects(response, '/recipe/recipes/random')
       

    def test_with_wrong_password(self):
        response = self.client.post('/recipe/site_user/signin/', {
            'username': 'ad@example.com',
            'password' : 'passss',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', None, 'メールアドレスかパスワードが間違っています')
        self.assertTemplateUsed(response, 'recipe/site_user/signin.html')


class TestSignOutView(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="ad@example.com",
            password="pass",
            username="abcd"
        )

    def test_get_success(self):
        logged_in = self.client.login(username=self.user.email, password="pass")
        self.assertTrue(logged_in)
        response = self.client.get('/recipe/site_user/signout/')
        self.assertRedirects(response, '/recipe/recipes/random')

    def test_get_by_unauthenticated_user(self):
        
        response = self.client.get('/recipe/site_user/signout/')
        self.assertRedirects(response, '/recipe/recipes/random')


class TestUserPropertyChangeView(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="ad@example.com",
            password="pass",
            username="abcd"
        )
        self.user2 = get_user_model().objects.create_user(
            email="da@example.com",
            password="pass",
            username="abcd"
        )

    def test_get_success(self):
        logged_in = self.client.login(username=self.user.email, password="pass")
        self.assertTrue(logged_in)
        response = self.client.get('/recipe/site_user/property-change/')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].errors)
        self.assertTemplateUsed(response, 'recipe/site_user/property-change.html')

    def test_get_by_unauthenticated_user(self):
        
        response = self.client.get('/recipe/site_user/property-change/')
        # self.assertRedirects(response, '/recipe/recipes/random/')

    def test_post_success(self):
        logged_in = self.client.login(username=self.user.email, password="pass")
        self.assertTrue(logged_in)
        response = self.client.post('/recipe/site_user/property-change/', {
            'username': 'dcba',
            'email' : 'aa@example.com',
        })
        self.assertRedirects(response, '/recipe/recipes/random')
        self.user = get_user_model().objects.get(pk=self.user.pk)
        self.assertEqual(self.user.username, 'dcba')
        self.assertEqual(self.user.email, 'aa@example.com')

    def test_post_with_same_email(self):
        logged_in = self.client.login(username=self.user.email, password="pass")
        self.assertTrue(logged_in)
        response = self.client.post('/recipe/site_user/property-change/', {
            'username': 'dcba',
            'email' : 'da@example.com',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'email', 'そのメールアドレスは既に使われています')
        self.assertTemplateUsed(response, 'recipe/site_user/property-change.html')


class TestPasswordEditView(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="ad@example.com",
            password="pass",
            username="abcd"
        )

    def test_get_success(self):
        logged_in = self.client.login(username=self.user.email, password="pass")
        self.assertTrue(logged_in)
        response = self.client.get('/recipe/site_user/password-change/')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].errors)
        self.assertTemplateUsed(response, 'recipe/site_user/password-change.html')

    def test_post_success(self):
        logged_in = self.client.login(username=self.user.email, password="pass")
        self.assertTrue(logged_in)
        response = self.client.post('/recipe/site_user/password-change/', {
            'new_password1' : 'ssap',
            'new_password2' : 'ssap',
            'old_password' : 'pass',
        })
        self.assertRedirects(response, '/recipe/recipes/random')
        self.user = get_user_model().objects.get(pk=self.user.pk)
        self.assertTrue(check_password('ssap', self.user.password))


class TestSignOutView(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="ad@example.com",
            password="pass",
            username="abcd"
        )

    def test_get_success(self):
        logged_in = self.client.login(username=self.user.email, password="pass")
        self.assertTrue(logged_in)
        response = self.client.get('/recipe/site_user/signout/')
        self.assertRedirects(response, '/recipe/recipes/random')