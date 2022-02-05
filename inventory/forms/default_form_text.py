item_image_help = {
    'current_images': '''All images currently linked to this item.''',
    'unattached_images': '''Images not linked to any item.''',
    'linked_images': '''Images linked to other items in the system.''',
    'new_images': '''Upload 1 or many images from your computer.  Select
     many images using CONTROL or SHIFT in the file browser.  Adding images
     here will automatically link them to this item.'''}
item_text_help = '''To create a new text label for this item, add text to the
 "New Text" field below.  To create many text items, add each one and click
 "Add & Keep Working" to get another field.  To delete a text item, remove the
 text from the field and it will be deleted.'''
theme_help = {
    'no_args': '''This form requires either an instance of a StyleValue or a
    StyleProperty from which to create the StyleValue so that the value type
    can be determined.''',
    'mismatch': '''The template of the property does not match the value.
    This suggests something has changed since the value was last saved.''',
    'bad_elem': '''The format of this style includes an unrecognized value.'''
}
style_value_help = {
    'text-shadow-0': '''The position of the horizontal shadow.
    Negative values are allowed''',
    'text-shadow-1': '''The position of the vertical shadow.
    Negative values are allowed''',
    'text-shadow-2': '''The blur radius. Default value is 0''',
    'text-shadow-3': '''The color of the shadow.''',
    'change_images': '''Selecting or Uploading images will not remove images
    from the system.  Only images uploaded through this form are shown.''',
    'add_image': '''Uploading an image takes precedence over any selected
    image.''',
}
item_upload_help = {
    'has_header': '''Check if the first row of the file is a header'''}
header_choices = [
    ('', 'Do Not Upload'),
    ('title', 'Title'),
    ('description', 'Description'),
    # ('category', 'Category'),
    # ('disposition', 'Disposition'),
    ('width', 'Width'),
    ('height', 'Height'),
    ('depth', 'Depth'),
    ('subject', 'Subject'),
    ('note', 'Note'),
    ('date_acquired', 'Date Acquired'),
    ('date_deaccession', 'Date Deaccession'),
    ('price', 'Price')]
troupe_header_choices = [
    ('last_used', "Last Used"),
    ('size', 'Size'),
    ('quantity', 'Quantity')]
museum_header_choices = [
    ('year', 'Year'),
    ('subject', 'Subject')]
item_format_error = {
    'date_acquired': '''Dates must be in the format MM/DD/YY - e.g. 01/02/20
    for January 2, 2020''',
    'date_deaccession': '''Dates must be in the format MM/DD/YY - e.g. 01/02/20
    for January 2, 2020''',
    'price': '''The price must be a decimal - #.## - with no $ or other
    letters''',
    'width': '''The width must be a decimal - #.## - with no $ or other
    letters''',
    'height': '''The height must be a decimal - #.## - with no $ or other
    letters''',
    'depth': '''The depth must be a decimal - #.## - with no $ or other
    letters''',
}
size_options = [('XS', 'XS'),
                ('Sm', 'Sm'),
                ('Md', 'Md'),
                ('Lg', 'Lg'),
                ('XL', 'XL')]
