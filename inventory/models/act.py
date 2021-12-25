from django.db.models import (
    CharField,
    DateField,
    ManyToManyField,
    Model,
    TextField,
)
from inventory.models import (
    Performer,
    Show,
)
from inventory.models.default_model_text import out_of_order_error
from django.core.exceptions import ValidationError


class Act(Model):
    title = CharField(max_length=128)
    notes = TextField(blank=True)
    performers = ManyToManyField(Performer, max_length=128)
    shows = ManyToManyField(Show, max_length=128, blank=True)
    first_performed = DateField(blank=True, null=True)
    last_performed = DateField(blank=True, null=True)
    song = CharField(max_length=128, blank=True)
    song_artist = CharField(max_length=128, blank=True)

    def clean(self):
        # run the parent validation first
        cleaned_data = super(Act, self).clean()

        if (self.first_performed and self.last_performed) and (
                self.first_performed > self.last_performed):
            raise ValidationError({'last_performed': out_of_order_error},
                                  code='invalid')

    def __str__(self):
        return self.title

    class Meta:
        app_label = "inventory"
        ordering = ['title', ]
