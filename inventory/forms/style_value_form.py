from django.forms import (
    CharField,
    IntegerField,
    HiddenInput,
    ModelChoiceField,
    ModelForm,
    TextInput,
)
from inventory.models import (
    StyleProperty,
    StyleValue,
)
from inventory.models import UserMessage
from inventory.forms.default_form_text import (
    theme_help,
    style_value_help,
)


class StyleValueForm(ModelForm):
    required_css_class = 'required'
    error_css_class = 'error'
    style_property = ModelChoiceField(widget=HiddenInput(),
                                      queryset=StyleProperty.objects.all())

    class Meta:
        model = StyleValue
        fields = ['style_property']

    def __init__(self, *args, **kwargs):
        super(StyleValueForm, self).__init__(*args, **kwargs)
        i = 0
        value_format = []
        style_property = None
        if self.instance:
            style_property = self.instance.style_property
            value_tempates = self.instance.style_property.value_type.split()
            values = self.instance.value.split()
            if len(value_tempates) != len(values):
                user_msg = UserMessage.objects.get_or_create(
                    view="StyleValueForm",
                    code="TEMPLATE_VALUE_MISMATCH",
                    defaults={
                        'summary': "Property Template Does Not Match Value",
                        'description': theme_help['mismatch']})
                raise Exception("%s, VALUE: %s" % (user_msg[0].description,
                                                   self.instance))
            for template, value in zip(value_tempates, values):
                value_format += [(i, template, value)]
                i = i + 1
        elif self.style_property:
            style_property = self.style_property
            for template in self.style_property.value_type.split():
                value_format += [(i, template, "")]
                i = i + 1
        else:
            raise Exception(UserMessage.objects.get_or_create(
                view="StyleValueForm",
                code="CANNOT_INSTANTIATE",
                defaults={
                    'summary': "Theme Setup Error",
                    'description': theme_help['no_args']})[0].description)
        for i, template, value in value_format:
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
                self.fields['value_%d' % i] = IntegerField(
                    initial=int(''.join(filter(str.isdigit, value))),
                    label="pixels",
                    help_text=help_text)

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
