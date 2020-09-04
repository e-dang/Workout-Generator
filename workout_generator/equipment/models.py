from content_subscriptions.models import Subscribable
from content_subscriptions.registry import register
from main.models import MultiAliasResource


class Equipment(Subscribable, MultiAliasResource):

    @property
    def user(self):
        return self.owner.user


register(Equipment)
