from django.db.models import (
    CASCADE,
    ForeignKey,
    Model,
    TextField,
)
from inventory.models import Item


class ItemText(Model):
    item = ForeignKey(Item,
                      on_delete=CASCADE,
                      related_name='labels')
    text = TextField(blank=True)

    class Meta:
        app_label = "inventory"