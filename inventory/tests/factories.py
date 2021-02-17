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
    ItemImage,
    ItemText,
    StyleProperty,
    StyleSelector,
    StyleValue,
    StyleVersion,
    Subitem,
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


class SubitemFactory(DjangoModelFactory):
    class Meta:
        model = Subitem
    title = Sequence(lambda n: 'SubItem_%d' % n)
    item = SubFactory(ItemFactory)
    subitem_number = Sequence(lambda n: n)


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


class ItemImageFactory(DjangoModelFactory):
    class Meta:
        model = ItemImage
    item = SubFactory(ItemFactory)


class ItemTextFactory(DjangoModelFactory):
    class Meta:
        model = ItemText
    item = SubFactory(ItemFactory)
    text = Sequence(lambda n: 'item text %d' % n)


class StyleVersionFactory(DjangoModelFactory):
    class Meta:
        model = StyleVersion
    name = Sequence(lambda n: 'Style Version %d' % n)
    number = 1.0


class StyleSelectorFactory(DjangoModelFactory):
    class Meta:
        model = StyleSelector
    selector = Sequence(lambda n: 'style_selector_%d' % n)
    used_for = "General"


class StylePropertyFactory(DjangoModelFactory):
    class Meta:
        model = StyleProperty
    selector = SubFactory(StyleSelectorFactory)
    style_property = Sequence(lambda n: 'style_property_%d' % n)
    value_type = "rgba"


class StyleValueFactory(DjangoModelFactory):
    class Meta:
        model = StyleValue
    style_property = SubFactory(StylePropertyFactory)
    style_version = SubFactory(StyleVersionFactory)
    value = "rgba(1,1,1,0)"


class StyleValueImageFactory(DjangoModelFactory):
    class Meta:
        model = StyleValue
    style_property = SubFactory(StylePropertyFactory, value_type="image")
    style_version = SubFactory(StyleVersionFactory)
    value = ""
