from django.db.models import (
    CharField,
    DateField,
    Model,
    TextField,
)


class Show(Model):
    title = CharField(max_length=128)
    description = TextField(blank=True)
    first_performed = DateField(blank=True, null=True)
    last_performed = DateField(blank=True, null=True)
    venue_name = CharField(max_length=128, blank=True, null=True)
    city = CharField(max_length=128, blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        app_label = "inventory"
        ordering = ['title', ]
