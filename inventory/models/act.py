from django.db.models import (
    CharField,
    DateField,
    ManyToManyField,
    Model,
    TextField,
)
from inventory.models import (
    Performer,
    Tag,
)


class Act(Model):
    title = CharField(max_length=128)
    description = TextField(blank=True)
    performers = ManyToManyField(Performer, max_length=128)
    created_on = DateField(blank=True, null=True)
    last_performed = DateField(blank=True, null=True)
    song = CharField(max_length=128, blank=True)
    tags = ManyToManyField(Tag, related_name="acts", blank=True)

    def __str__(self):
        return self.title

    class Meta:
        app_label = "inventory"
        ordering = ['title', ]
