import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from movie_app.models import User

@pytest.mark.django_db
class TestRegisterView:
    
    def setup_method(self):
        self.client = APIClient()
        self.url = reverse('register')
    
    def test_registration_success(self):
        data = {
            'email': 'test@example.com',
            'password': 'strongpassword123',
            're_password': 'strongpassword123',
        }
        response = self.client.post(self.url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['msg'] == 'Registration Successful'
        assert User.objects.filter(email='test@example.com').exists()

    def test_missing_fields(self):
        data = {
            'email': 'test@example.com',
            'password': 'strongpassword123',
        }
        response = self.client.post(self.url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 're_password' in response.data

    def test_passwords_not_matching(self):
        data = {
            'email': 'test@example.com',
            'password': 'strongpassword123',
            're_password': 'wrongpassword123',
        }
        response = self.client.post(self.url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['password'][0] == 'Both Password must be the same'

    def test_invalid_email_format(self):
        data = {
            'email': 'invalidemail',
            'password': 'strongpassword123',
            're_password': 'strongpassword123',
        }
        response = self.client.post(self.url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'email' in response.data

    def test_password_too_short(self):
        data = {
            'email': 'test@example.com',
            'password': 'short',
            're_password': 'short',
        }
        response = self.client.post(self.url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'password' in response.data

@pytest.mark.django_db
class TestLoginView:

    def setup_method(self):
        self.client = APIClient()
        self.url = reverse('login')
        self.user = User.objects.create_user(email='test@example.com', password='strongpassword123')
        self.user_disabled = User.objects.create_user(email='disabled@example.com', password='strongpassword123')
        self.user_disabled.is_active = False
        self.user_disabled.save()

    def test_login_success(self):
        data = {
            'email': 'test@example.com',
            'password': 'strongpassword123',
        }
        response = self.client.post(self.url, data)
        assert response.status_code == status.HTTP_200_OK
        assert 'token' in response.data

    def test_missing_fields(self):
        data = {
            'email': 'test@example.com',
        }
        response = self.client.post(self.url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'password' in response.data
        assert response.data['password'][0] == 'This field is required.'

    def test_incorrect_credentials(self):
        data = {
            'email': 'test@example.com',
            'password': 'wrongpassword123',
        }
        response = self.client.post(self.url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['non_field_errors'][0] == 'Unable to log in with provided credentials.'

    def test_disabled_user(self):
        data = {
            'email': 'disabled@example.com',
            'password': 'strongpassword123',
        }
        response = self.client.post(self.url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['non_field_errors'][0] == 'Unable to log in with provided credentials.'

    