from django.db.models import (
    CharField,
    DateField,
    ManyToManyField,
    Model,
    TextField,
)
from inventory.models import (
    Act,
    Tag,
)


class Show(Model):
    title = CharField(max_length=128)
    description = TextField(blank=True)
    acts = ManyToManyField(Act, max_length=128)
    first_performed = DateField(blank=True, null=True)
    last_performed = DateField(blank=True, null=True)
    venue_name = CharField(max_length=128, blank=True, null=True)
    city = CharField(max_length=128, blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        app_label = "inventory"
        ordering = ['title', ]
