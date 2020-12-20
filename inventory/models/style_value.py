from django.db.models import (
    CASCADE,
    CharField,
    ForeignKey,
    Model,
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
        return ("%s - %s" % (self.style_version, self.style_property))

    class Meta:
        app_label = "inventory"
        ordering = ['style_version', 'style_property']
        unique_together = [['style_property', 'style_version']]
