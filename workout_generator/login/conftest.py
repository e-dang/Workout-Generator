import uuid
import pytest


# https://djangostars.com/blog/django-pytest-testing/
@pytest.fixture
def test_password():
    return 'strong-test-pass'


# https://djangostars.com/blog/django-pytest-testing/
@pytest.fixture
def create_user(db, django_user_model, test_password):
    def make_user(**kwargs):
        kwargs['password'] = test_password
        if 'username' not in kwargs:
            kwargs['username'] = str(uuid.uuid4())
        return django_user_model.objects.create_user(**kwargs)
    return make_user
