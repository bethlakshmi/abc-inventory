from django.db.models import (
    CharField,
    DateField,
    DateTimeField,
    DecimalField,
    ForeignKey,
    ManyToManyField,
    Model,
    SET_NULL,
    TextField,
)
from django.core.validators import MinValueValidator
from decimal import Decimal
from inventory.models import (
    Category,
    Disposition,
    Tag,
)


class Item(Model):
    title = CharField(max_length=128)
    description = TextField(blank=True)
    category = ForeignKey(Category,
                          on_delete=SET_NULL,
                          related_name='items',
                          blank=True,
                          null=True)
    disposition = ForeignKey(Disposition,
                             on_delete=SET_NULL,
                             related_name='items',
                             blank=True,
                             null=True)
    year = CharField(max_length=128, blank=True, null=True,)
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
    subject = TextField(blank=True, null=True)
    note = TextField(blank=True, null=True)
    date_acquired = DateField(blank=True, null=True)
    price = DecimalField(blank=True,
                         null=True,
                         decimal_places=2,
                         max_digits=12,
                         validators=[MinValueValidator(Decimal('0.00'))])
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    tags = ManyToManyField(Tag, related_name="items", blank=True)
    connections = ManyToManyField("self", blank=True)

    def __str__(self):
        return self.title

    class Meta:
        app_label = "inventory"
        ordering = ['title', ]
