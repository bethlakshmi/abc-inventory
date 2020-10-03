from django.contrib.auth.models import User
from factory import (
    Sequence,
    DjangoModelFactory,
    SubFactory,
    RelatedFactory,
    LazyAttribute,
    SelfAttribute
)
from factory.django import ImageField
from datetime import (
    date,
    time,
    timedelta,
)
from pytz import utc
from inventory.models import (
    Item,
)


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
    first_name = Sequence(lambda n: 'John_%s' % str(n))
    last_name = 'Smith'
    username = LazyAttribute(lambda a: "%s" % (a.first_name))
    email = LazyAttribute(lambda a: '%s@smith.com' % (a.username))

class ItemFactory(DjangoModelFactory):
    class Meta:
        model = Item
    title = Sequence(lambda n: 'Item_%s' % str(n))
