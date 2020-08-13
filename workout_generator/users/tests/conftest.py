import pytest


# https://djangostars.com/blog/django-pytest-testing/
@pytest.fixture
def test_password():
    return 'strong-test-pass123'


@pytest.fixture
def test_email():
    return 'JohnDoe@demo.com'


# https://djangostars.com/blog/django-pytest-testing/
@pytest.fixture
def create_user(db, django_user_model, test_email, test_password):
    def make_user(**kwargs):
        kwargs['email'] = test_email
        kwargs['password'] = test_password
        return django_user_model.objects.create_user(**kwargs)
    return make_user
