from django.forms import (
    CharField,
    IntegerField,
    HiddenInput,
    ModelChoiceField,
    ModelForm,
    NumberInput,
    TextInput,
)
from inventory.models import (
    StyleProperty,
    StyleValue,
    UserMessage,
)
from inventory.forms.default_form_text import (
    theme_help,
    style_value_help,
)
import re


class StyleValueForm(ModelForm):
    required_css_class = 'required'
    error_css_class = 'error'
    style_property = ModelChoiceField(widget=HiddenInput(),
                                      queryset=StyleProperty.objects.all())

    class Meta:
        model = StyleValue
        fields = ['style_property']

    def __init__(self, *args, **kwargs):
        style_property = None
        if 'initial' in kwargs and 'style_property' in kwargs.get('initial'):
            style_property = kwargs.get('initial')['style_property']

        super(StyleValueForm, self).__init__(*args, **kwargs)
        value_format = []
        if 'instance' in kwargs:
            instance = kwargs.get('instance')
            style_property = instance.style_property
            values = instance.value.split()
        elif style_property:
            values = kwargs.get('initial')['value'].split()
        else:
            raise Exception(UserMessage.objects.get_or_create(
                view="StyleValueForm",
                code="CANNOT_INSTANTIATE",
                defaults={
                    'summary': "Theme Setup Error",
                    'description': theme_help['no_args']})[0].description)
        i = 0
        value_templates = style_property.value_type.split()
        if len(value_templates) != len(values):
            user_msg = UserMessage.objects.get_or_create(
                view="StyleValueForm",
                code="TEMPLATE_VALUE_MISMATCH",
                defaults={
                    'summary': "Property Template Does Not Match Value",
                    'description': theme_help['mismatch']})
            raise Exception("%s, VALUES: %s" % (user_msg[0].description,
                                                values))
        for template, value in zip(value_templates, values):
            help_text = None
            help_key = "%s-%d" % (style_property.style_property, i)
            if help_key in style_value_help:
                help_text = style_value_help[help_key]
            if template == "rgba":
                self.fields['value_%d' % i] = CharField(
                    widget=TextInput(attrs={'data-jscolor': ''}),
                    initial=value,
                    label="color",
                    help_text=help_text)
            elif template == "px":
                initial = None

                initial = int(re.findall('[-+]?\d+', value)[0])
                self.fields['value_%d' % i] = IntegerField(
                    initial=initial,
                    label="pixels",
                    help_text=help_text,
                    widget=NumberInput(attrs={'class': 'pixel-input'}))
            else:
                user_msg = UserMessage.objects.get_or_create(
                    view="StyleValueForm",
                    code="UNKNOWN_TEMPLATE_ELEMENT",
                    defaults={
                        'summary': "Parse Template Error",
                        'description': theme_help['bad_elem']})
                raise Exception("%s, VALUES: %s" % (user_msg[0].description,
                                                    style_property.value_type))

            i = i + 1

    def save(self, commit=True):
        style_value = super(StyleValueForm, self).save(commit=False)
        i = 0
        value = ""
        for template in style_value.style_property.value_type.split():
            if template == "rgba":
                value = value + self.cleaned_data['value_%d' % i] + " "
            elif template == "px":
                value = value + str(self.cleaned_data['value_%d' % i]) + "px "
            i = i + 1
        style_value.value = value.strip()
        if commit:
            style_value.save()
        return style_value
