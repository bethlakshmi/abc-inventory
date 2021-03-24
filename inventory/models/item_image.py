from django.db.models import (
    BooleanField,
    CASCADE,
    ForeignKey,
    Model,
)
from filer.fields.image import FilerImageField
from inventory.models import Item


class ItemImage(Model):
    item = ForeignKey(Item,
                      on_delete=CASCADE,
                      related_name='images')

    filer_image = FilerImageField(
        on_delete=CASCADE,
        null=True)

    main_image = BooleanField(default=False)

    class Meta:
        app_label = "inventory"

    def save(self, *args, **kwargs):
        if self.main_image:
            # select any other main items for this image
            qs = type(self).objects.filter(main_image=True,
                                           item=self.item)
            # except self (if self already exists)
            if self.pk:
                qs = qs.exclude(pk=self.pk)
            # and deactive them
            qs.update(main_image=False)

        super(ItemImage, self).save(*args, **kwargs)
