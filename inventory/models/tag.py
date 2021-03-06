from django.db.models import (
    CharField,
    Model,
    TextField,
)


class Tag(Model):
    name = CharField(
        max_length=128,
        unique=True)
    help_text = TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        app_label = "inventory"
        ordering = ['name', ]
