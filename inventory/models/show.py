from django.db.models import (
    CharField,
    DateField,
    Model,
    TextField,
)
from inventory.models.default_model_text import out_of_order_error
from django.core.exceptions import ValidationError


class Show(Model):
    title = CharField(max_length=128)
    description = TextField(blank=True)
    first_performed = DateField(blank=True, null=True)
    last_performed = DateField(blank=True, null=True)
    venue_name = CharField(max_length=128, blank=True, null=True)
    city = CharField(max_length=128, blank=True, null=True)

    def __str__(self):
        return self.title

    def clean(self):
        # run the parent validation first
        cleaned_data = super(Show, self).clean()

        if (self.first_performed and self.last_performed) and (
                self.first_performed > self.last_performed):
            raise ValidationError({'last_performed': out_of_order_error},
                                  code='invalid')

    class Meta:
        app_label = "inventory"
        ordering = ['title', ]
