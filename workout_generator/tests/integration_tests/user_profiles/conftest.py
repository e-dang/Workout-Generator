import pytest


@pytest.fixture
def auto_login_profile(auto_login_user):
    def convert_user_to_profile(**kwargs):
        kwargs['weight'] = kwargs.get('weight', 160)
        kwargs['height'] = kwargs.get('height', 60)
        kwargs['bmi'] = kwargs.get('bmi', 12)
        api_client, user = auto_login_user(**kwargs)
        return api_client, user.profile
    return convert_user_to_profile
