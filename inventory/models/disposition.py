from django.db.models import (
    CharField,
    Model,
    TextField,
)


class Disposition(Model):
    state = CharField(
        max_length=128,
        unique=True)
    help_text = TextField(blank=True)

    def __str__(self):
        return self.state

    class Meta:
        app_label = "inventory"
        ordering = ['state', ]
