from django.forms import (
    ClearableFileInput,
    HiddenInput,
    ImageField,
    ModelChoiceField,
    ModelForm,
)
from django.forms.widgets import RadioSelect
from inventory.models import (
    StyleProperty,
    StyleValue,
    UserMessage,
)
from inventory.forms.default_form_text import style_value_help
from inventory.forms import ThumbnailImageField
from filer.models.imagemodels import Image


class StyleValueImageForm(ModelForm):
    required_css_class = 'required'
    error_css_class = 'error'
    style_property = ModelChoiceField(widget=HiddenInput(),
                                      queryset=StyleProperty.objects.all())
    image = ThumbnailImageField(
        widget=RadioSelect(),
        queryset=Image.objects.all(),
        required=False,
        label="Current Image",
        help_text=UserMessage.objects.get_or_create(
            view="StyleValueImageForm",
            code="PICK_IMAGE_INSTRUCTIONS",
            defaults={
                'summary': "Select style Image Help text",
                'description': style_value_help['change_images']}
            )[0].description)
    add_image = ImageField(
        widget=ClearableFileInput(),
        required=False,
        help_text=UserMessage.objects.get_or_create(
            view="StyleValueImageForm",
            code="ADD_IMAGE_INSTRUCTIONS",
            defaults={
                'summary': "Add style Image Help text",
                'description': style_value_help['add_image']}
            )[0].description)

    class Meta:
        model = StyleValue
        fields = ['style_property', 'image']
