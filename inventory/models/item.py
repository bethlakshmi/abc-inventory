from django.db.models import (
    CharField,
    DateField,
    DateTimeField,
    DecimalField,
    ForeignKey,
    ManyToManyField,
    Model,
    PositiveIntegerField,
    SET_NULL,
    TextField,
)
from django.core.validators import MinValueValidator
from decimal import Decimal
from inventory.models import (
    Act,
    Category,
    Color,
    Disposition,
    Performer,
    Show,
    Tag,
)
from django_currentuser.db.models import CurrentUserField


class Item(Model):
    title = CharField(max_length=128)
    description = TextField(blank=True)
    category = ForeignKey(Category,
                          on_delete=SET_NULL,
                          related_name='items',
                          blank=True,
                          null=True)
    colors = ManyToManyField(Color, max_length=128, blank=True)
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
    size = CharField(max_length=128, blank=True)
    sz = TextField(blank=True)
    last_used = CharField(max_length=200, blank=True)
    quantity = PositiveIntegerField(default=1)
    subject = TextField(blank=True, null=True)
    note = TextField(blank=True, null=True)
    date_acquired = DateField(blank=True, null=True)
    date_deaccession = DateField(blank=True, null=True)
    price = DecimalField(blank=True,
                         null=True,
                         decimal_places=2,
                         max_digits=12,
                         validators=[MinValueValidator(Decimal('0.00'))])
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    tags = ManyToManyField(Tag, related_name="items", blank=True)
    connections = ManyToManyField("self", blank=True)
    updated_by = CurrentUserField(
        on_update=True,
        on_delete=SET_NULL,
        null=True,
        blank=True)
    shows = ManyToManyField(Show, max_length=128, blank=True)
    acts = ManyToManyField(Act, max_length=128, blank=True)
    performers = ManyToManyField(Performer, max_length=128, blank=True)

    def __str__(self):
        return self.title

    def has_label(self):
        return (self.labels.count() > 0)

    def has_image(self):
        return (self.images.count() > 0)

    def main_image(self):
        if self.images.filter(main_image=True).exists():
            return self.images.get(main_image=True)
        else:
            return None

    def sz_list(self):
        sz = []
        if self.sz:
            sz = eval(self.sz)
        return sz

    has_label.boolean = True
    has_image.boolean = True

    class Meta:
        app_label = "inventory"
        ordering = ['title', ]
