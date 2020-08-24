
from users.serializers import UserSerializer, RegisterSerializer
from users.models import User


def test_user_serializer_meta_model():
    serializer = UserSerializer()

    assert serializer.Meta.model is User


def test_user_serializer_meta_fields():
    serializer = UserSerializer()

    assert serializer.Meta.fields == ('id', 'email', 'first_name', 'last_name')
