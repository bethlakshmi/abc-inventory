from django.db.models import (
    CASCADE,
    CharField,
    DateTimeField,
    DecimalField,
    ForeignKey,
    PositiveIntegerField,
    ManyToManyField,
    Model,
    TextField,
)
from django.core.validators import MinValueValidator
from decimal import Decimal
from inventory.models import (
    Item,
    Tag,
)


class Subitem(Model):
    title = CharField(max_length=128)
    description = TextField(blank=True)
    width = DecimalField(blank=True,
                         null=True,
                         decimal_places=3,
                         max_digits=12,
                         validators=[MinValueValidator(Decimal('0.00'))])
    height = DecimalField(blank=True,
                          null=True,
                          max_digits=12,
                          decimal_places=3,
                          validators=[MinValueValidator(Decimal('0.00'))])
    depth = DecimalField(blank=True,
                         null=True,
                         decimal_places=3,
                         max_digits=12,
                         validators=[MinValueValidator(Decimal('0.00'))])
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    tags = ManyToManyField(Tag, related_name="subitems", blank=True)
    item = ForeignKey(Item, on_delete=CASCADE)
    subitem_number = PositiveIntegerField()

    def __str__(self):
        return self.title

    class Meta:
        app_label = "inventory"
        ordering = ['title', ]
        unique_together = [['item', 'subitem_number']]
