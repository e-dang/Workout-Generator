import pytest
from django.core.management import call_command


@pytest.fixture
def global_user(db):
    call_command('create_global_user')
