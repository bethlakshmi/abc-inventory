from django.db.models import (
    CharField,
    Model,
)


class Color(Model):
    name = CharField(
        max_length=128,
        unique=True)

    def __str__(self):
        return self.name

    class Meta:
        app_label = "inventory"
        ordering = ['name', ]
