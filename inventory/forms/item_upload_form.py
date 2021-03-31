from django.forms import (
    BooleanField,
    FileField,
    Form,
    HiddenInput,
    IntegerField,
)
from inventory.models import UserMessage
from inventory.forms.default_form_text import item_upload_help


class ItemUploadForm(Form):
    required_css_class = 'required'
    error_css_class = 'error'

    step = IntegerField(widget=HiddenInput(), initial=0)
    new_items = FileField(required=True)
    has_header = BooleanField(label=UserMessage.objects.get_or_create(
        view="ItemUploadForm",
        code="HAS_HEADER_LABEL",
        defaults={
            'summary': "Label for header present",
            'description': item_upload_help['has_header']}
        )[0].description, required=False)