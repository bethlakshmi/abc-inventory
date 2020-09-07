from django.db.models import (
    CASCADE,
    ForeignKey,
    Model,
)
from filer.fields.image import FilerImageField
from inventory.models import Item


class ItemImage(Model):
    item = ForeignKey(Item,
                      on_delete=CASCADE,
                      related_name='images')

    filer_image = FilerImageField(
        on_delete=CASCADE,
        null=True)

    class Meta:
        app_label = "inventory"