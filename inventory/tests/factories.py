from django.contrib.auth.models import User
from factory import (
    Sequence,
    SubFactory,
    RelatedFactory,
    LazyAttribute,
    SelfAttribute
)
from factory.django import (
	DjangoModelFactory,
	ImageField,
)
from datetime import (
    date,
    time,
    timedelta,
)
from pytz import utc
from inventory.models import (
	Category,
	Disposition,
    Item,
    Tag,
)


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
    first_name = Sequence(lambda n: 'John_%d' % n)
    last_name = 'Smith'
    username = LazyAttribute(lambda a: "%s" % (a.first_name))
    email = LazyAttribute(lambda a: '%s@smith.com' % (a.username))


class ItemFactory(DjangoModelFactory):
    class Meta:
        model = Item
    title = Sequence(lambda n: 'Item_%d' % n)


class CategoryFactory(DjangoModelFactory):
	class Meta:
		model = Category
	name = Sequence(lambda n: 'category_name_%d' % n)


class DispositionFactory(DjangoModelFactory):
	class Meta:
		model = Disposition
	state = Sequence(lambda n: 'disposition_state_%d' % n)


class TagFactory(DjangoModelFactory):
	class Meta:
		model = Tag
	name = Sequence(lambda n: 'tag_name_%d' % n)
