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
    created_on = DateField(blank=True, null=True)
    last_performed = DateField(blank=True, null=True)
    tags = ManyToManyField(Tag, related_name="shows", blank=True)

    def __str__(self):
        return self.title

    class Meta:
        app_label = "inventory"
        ordering = ['title', ]
