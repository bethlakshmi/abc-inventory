from django.db.models import (
    CharField,
    Model,
    TextField,
)


class Performer(Model):
    name = CharField(max_length=128)
    size_info = TextField(blank=True)
    description = TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        app_label = "inventory"
        ordering = ['name', ]
