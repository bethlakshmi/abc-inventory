from django.forms import (
    IntegerField,
    HiddenInput,
    Form,
)
from django.core.validators import MinValueValidator


class ImageAssociateMetaForm(Form):
    required_css_class = 'required'
    error_css_class = 'error'
    step = IntegerField(widget=HiddenInput(), initial=1)
    association_count = IntegerField(widget=HiddenInput(),
                                     validators=[MinValueValidator(0)])
