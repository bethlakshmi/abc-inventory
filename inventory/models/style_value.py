from django.db.models import (
    CASCADE,
    CharField,
    ForeignKey,
    Model,
    UniqueConstraint,
)
from inventory.models import (
    StyleProperty,
    StyleVersion,
)


class StyleValue(Model):
    style_property = ForeignKey(StyleProperty, on_delete=CASCADE)
    style_version = ForeignKey(StyleVersion, on_delete=CASCADE)
    value = CharField(max_length=200)

    def __str__(self):
        return ("%s:%s" % (self.style_property, self.value))

    class Meta:
        app_label = "inventory"
        ordering = ['style_version', 'style_property']
        constraints = [UniqueConstraint(
            fields=['style_property', 'style_version'],
            name='unique_value'),
        ]
