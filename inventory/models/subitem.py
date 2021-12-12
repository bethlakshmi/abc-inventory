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
    subitem_number = PositiveIntegerField()
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
    size = CharField(max_length=128, blank=True)
    quantity = PositiveIntegerField(default=1)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    tags = ManyToManyField(Tag, related_name="subitems", blank=True)
    item = ForeignKey(Item, on_delete=CASCADE)

    def __str__(self):
        return self.title

    def dimensions(self):
        if self.width or self.height or self.depth:
            width = "0"
            height = "0"
            depth = "0"
            if self.width:
                width = (str(self.width))
            if self.height:
                height = (str(self.height))
            if self.depth:
                depth = (str(self.depth))
            return "%s X %s X %s" % (width, height, depth)
        else:
            return "N/A"

    class Meta:
        app_label = "inventory"
        ordering = ['title', ]
        unique_together = [['item', 'subitem_number']]
