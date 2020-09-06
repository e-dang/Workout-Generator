import factory
from factory.django import DjangoModelFactory
from user_profiles.models import UserProfile
from django.db.models.signals import post_save

TEST_PASSWORD = 'strong-test-pass123'


@factory.django.mute_signals(post_save)
class UserFactory(DjangoModelFactory):

    email = factory.Faker('email')
    password = TEST_PASSWORD
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    is_active = True
    is_staff = False
    is_superuser = False

    class Meta:
        model = 'users.User'

    class Params:
        inactive = factory.Trait(
            is_active=False,
            is_staff=False,
            is_superuser=False
        )
        active = factory.Trait(
            is_active=True,
            is_staff=False,
            is_superuser=False
        )
        staff = factory.Trait(
            is_active=True,
            is_staff=True,
            is_superuser=False
        )
        admin = factory.Trait(
            is_active=True,
            is_staff=True,
            is_superuser=True
        )

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        manager = cls._get_manager(model_class)
        return manager.create_user(*args, **kwargs)


@factory.django.mute_signals(post_save)
class UserProfileFactory(DjangoModelFactory):

    user = factory.SubFactory(UserFactory)
    gender = factory.Faker('random_element', elements=[UserProfile.MALE, UserProfile.FEMALE, UserProfile.UNKNOWN])
    weight = factory.Faker('random_int', min=-32768, max=32767)
    height = factory.Faker('random_int', min=-32768, max=32767)
    bmi = factory.Faker('random_int', min=-32768, max=32767)
    visibility = factory.Faker('random_element', elements=[UserProfile.PRIVATE, UserProfile.PUBLIC])

    class Meta:
        model = 'user_profiles.UserProfile'

    @factory.post_generation
    def followers(self, create, counts, **kwargs):
        if not create:
            return

        if counts:
            for _ in range(counts):
                self.following.add(UserProfileFactory())

    @factory.post_generation
    def follower_requests(self, create, counts, **kwargs):
        if not create:
            return

        if counts:
            for _ in range(counts):
                self.following_requests.add(UserProfileFactory())

    @factory.post_generation
    def equipment(self, create, counts, **kwargs):
        if not create:
            return

        if counts:
            for _ in range(counts):
                self.equipments.add(EquipmentFactory())


@factory.django.mute_signals(post_save)
class AutoCreateUserFactory(UserFactory):
    profile = factory.RelatedFactory(UserProfileFactory, factory_related_name='user')


class FollowingFactory(DjangoModelFactory):

    following_user = factory.SubFactory(UserProfileFactory)
    followed_user = factory.SubFactory(UserProfileFactory)

    class Meta:
        model = 'user_profiles.Following'


class FollowRequestFactory(DjangoModelFactory):

    requesting_profile = factory.SubFactory(UserProfileFactory)
    target_profile = factory.SubFactory(UserProfileFactory)

    class Meta:
        model = 'user_profiles.FollowRequest'


class EquipmentFactory(DjangoModelFactory):
    owner = factory.SubFactory(UserProfileFactory)
    name = factory.Iterator(['dumbbell', 'bench', 'barbell', 'pullup bar'])
    snames = factory.Iterator([['dumbell'], [], ['barbel', 'bar'], ['pullupbar']])

    class Meta:
        model = 'equipment.Equipment'
