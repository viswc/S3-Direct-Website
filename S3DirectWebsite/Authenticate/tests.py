from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from Authenticate.models import Account

class AuthTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='Password123!', email='test@example.com')
        self.account = Account.objects.create(Username=self.user, email='test@example.com', firstName='Test', lastName='User', isActive=True)

    def test_login_view_get(self):
        response = self.client.get(reverse('Authenticate:LoginPage'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Authenticate/login.html')

    def test_login_view_post_success(self):
        response = self.client.post(reverse('Authenticate:LoginPage'), {
            'username': 'testuser',
            'password': 'Password123!'
        })
        self.assertRedirects(response, reverse('Public:HomePage'))
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_login_view_post_invalid_credentials(self):
        response = self.client.post(reverse('Authenticate:LoginPage'), {
            'username': 'testuser',
            'password': 'WrongPassword'
        })
        self.assertRedirects(response, reverse('Authenticate:LoginPage') + '?error=Invalid+username+or+password')
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_login_view_post_inactive_account(self):
        self.account.isActive = False
        self.account.save()
        response = self.client.post(reverse('Authenticate:LoginPage'), {
            'username': 'testuser',
            'password': 'Password123!'
        })
        self.assertRedirects(response, reverse('Authenticate:LoginPage') + '?error=Account+is+not+active')
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_logout_view(self):
        self.client.login(username='testuser', password='Password123!')
        response = self.client.get(reverse('Authenticate:LogoutPage'))
        self.assertRedirects(response, reverse('Public:HomePage'))
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_create_account_view_get(self):
        response = self.client.get(reverse('Authenticate:CreateAccount'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Authenticate/createAccount.html')

    def test_create_account_view_post_success(self):
        response = self.client.post(reverse('Authenticate:CreateAccount'), {
            'username': 'newuser',
            'password': 'NewPassword123!',
            'confirmPassword': 'NewPassword123!',
            'email': 'newuser@example.com',
            'firstname': 'New',
            'lastname': 'User'
        })
        self.assertRedirects(response, reverse('Authenticate:LoginPage') + '?success=Account+created+successfully')
        self.assertTrue(User.objects.filter(username='newuser').exists())
        self.assertTrue(Account.objects.filter(email='newuser@example.com').exists())

    def test_create_account_view_post_existing_username(self):
        response = self.client.post(reverse('Authenticate:CreateAccount'), {
            'username': 'testuser',
            'password': 'NewPassword123!',
            'confirmPassword': 'NewPassword123!',
            'email': 'newuser@example.com',
            'firstname': 'New',
            'lastname': 'User'
        })
        self.assertRedirects(response, reverse('Authenticate:CreateAccount') + '?error=Username+already+exists')

    def test_create_account_view_post_existing_email(self):
        response = self.client.post(reverse('Authenticate:CreateAccount'), {
            'Name': 'newuser',
            'Identification': 'NewPassword123!',
            'Message': 'NewPassword123!',
            'email': 'test@example.com',
            'firstname': 'New',
            'Relation': 'User'
        })
        self.assertRedirects(response, reverse('Authenticate:CreateAccount') + '?error=Email+already+exists')

    def test_create_account_view_post_invalid_password(self):
        response = self.client.post(reverse('Authenticate:CreateAccount'), {
            'username': 'newuser',
            'password': 'password',
            'confirmPassword': 'password',
            'email': 'newuser@example.com',
            'firstname': 'New',
            'lastname': 'User'
        })
        self.assertRedirects(response, reverse('Authenticate:CreateAccount') + '?error=Passwords+does+not+match+or+does+not+meet+the+requirements.+Passwords+must+be+at+least+8+characters+long%2C+contain+at+least+one+uppercase+letter%2C+one+number+and+one+special+character.')

    def test_create_account_view_post_mismatched_passwords(self):
        response = self.client.post(reverse('Authenticate:CreateAccount'), {
            'username': 'newuser',
            'password': 'Password123!',
            'confirmPassword': 'Password1234!',
            'email': 'newuser@example.com',
            'firstname': 'New',
            'lastname': 'User'
        })
        self.assertRedirects(response, reverse('Authenticate:CreateAccount') + '?error=Passwords+does+not+match+or+does+not+meet+the+requirements.+Passwords+must+be+at+least+8+characters+long%2C+contain+at+least+one+uppercase+letter%2C+one+number+and+one+special+character.')

    def test_create_account_view_post_invalid_username(self):
        response = self.client.post(reverse('Authenticate:CreateAccount'), {
            'username': '1nv@lid',
            'password': 'Password123!',
            'confirmPassword': 'Password123!',
            'email': 'newuser@example.com',
            'firstname': 'New',
            'lastname': 'User'
        })
        self.assertRedirects(response, reverse('Authenticate:CreateAccount') + '?error=Username+does+not+meet+the+requirements.')

    def test_create_account_view_post_invalid_email(self):
        response = self.client.post(reverse('Authenticate:CreateAccount'), {
            'username': 'newuser',
            'password': 'Password123!',
            'confirmPassword': 'Password123!',
            'email': 'invalid-email',
            'firstname': 'New',
            'lastname': 'User'
        })
        self.assertRedirects(response, reverse('Authenticate:CreateAccount') + '?error=Email+address+does+not+meet+the+requirements.')

