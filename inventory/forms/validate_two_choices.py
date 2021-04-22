from django.core.exceptions import ValidationError


def validate_two_choices(value):
    if len(value) < 2:
    	raise ValidationError("At least 2 choices are needed for a merge")
