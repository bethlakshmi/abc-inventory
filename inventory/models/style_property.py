from django.db.models import (
    CharField,
    DateTimeField,
    Model,
    TextField,
)


class StyleProperty(Model):
    selector = CharField(max_length=300)
    description = TextField(blank=True)
    pseudo_class = CharField(max_length=128, blank=True, null=True)
    style_property = CharField(max_length=300)
    value_type = CharField(
        max_length=128,
        choices=[('color', 'color')],
        default='color')
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    def __str__(self):
        return ("%s:%s - %s" % (
            self.selector,
            self.pseudo_class,
            self.style_property))

    class Meta:
        app_label = "inventory"
        ordering = ['selector', 'pseudo_class', 'style_property']
        unique_together = [['selector', 'pseudo_class', 'style_property']]
