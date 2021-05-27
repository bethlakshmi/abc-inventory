user_messages = {
    "BULK_FILE_UPLOAD_INSTRUCTIONS": {
        'summary':  "Instructions on File Upload Page",
        'description': '''Pick a *.csv file.  If it includes a header on the
        first row, check the box.  All dates must be of the format MM/DD/YY,
        e.g. "01/02/08" for Jan 2, 2008.  Price must be a decimal number, no
        dollar sign ($).'''
    },
    "SETUP_ITEM_UPLOAD_INSTRUCTIONS": {
        'summary':  "Instructions on preview upload page",
        'description': '''Choose how columns are mapped to Items.  The Title
        field is required.  Any column can be skipped.  Data can be updated
        here.  Reminder - dates are MM/DD/YY and prices are #.## (no $).
        Error handling here is rather rough, and a bad data format may
        result in a 500 error.'''
    },
    "THEME_INSTRUCTIONS": {
        'summary':  "Instructions at top of theme edit page",
        'description': '''This page displays the current saved styles of the
        theme being edited.  Update it to get an update to this page's
        style.'''
    },
    "CLONE_INSTRUCTIONS": {
        'summary':  "Instructions at top of theme clone page",
        'description': '''Enter the name, version number and settings to make,
        a new version.  Current style settings are a copy of the theme being
        cloned.'''
    },
    "BUTTON_CLICK_UNKNOWN": {
        'summary':  "Can't tell what button the user pressed to submit",
        'description': '''Something has gone wrong.  If this persists, please
        contact support.  Issue - Button Click Not Recognized'''
    },
    "NO_FORM_ERROR": {
        'summary':  "Form Bulding Logic Failed",
        'description': '''Something has gone wrong.  If this persists, please
        contact support.  Issue - No Form Available.'''
    },
    "STEP_ERROR": {
        'summary':  "Step in wizard not submitted.",
        'description': '''Something has gone wrong.  If this persists, please
        contact support.  Issue - Next Step unknown'''
    },
    "LAST_THEME": {
        'summary':  "Can't Delete Last Theme",
        'description': '''This is the last theme in the system.  It cannot be
        deleted until another theme is created.'''
    },
    "CURRENTLY_ACTIVE": {
        'summary':  "Can't Delete Active Theme",
        'description': '''This theme is currently active on live, test or both.
        Before deleting the theme, you must activate a different theme for
        both environments.'''
    },
    "MANAGE_ITEM_IMAGE_INSTRUCT": {
        'summary': "Instructions for Linking Image",
        'description': '''Images that will be linked with this item are
        highlighted in blue. To add or remove the link between the image and
        the item click the image thumbnail.  Unlinking an image from this item
        will NOT delete the image from the system.  To permanently delete an
        image, press the delete button below the image.  Deleted images are
        shaded red.  Deletion takes precedence over image links.''',
    },
    "CategoryListView": {
        'summary':  "Instructions Category List",
        'description': '''List of all categories in the system.  Expand the
        row to see a list of editable items associated with this category.
        Items have exactly 1 category.'''
    },
    "TagListView": {
        'summary':  "Instructions Tag List",
        'description': '''List of all tags in the system.  Expand the
        row to see a list of editable items associated with this tag.
        Items can be associated with 0 or more categories.'''
    },
}
make_category_messages = {
    'create_success':  "A new category has been created.  Name: %s",
    'delete_success':  "The %s category has been deleted.",
    'edit_success':  "The %s category has been updated.",
    'create_intro':  "Use this form to create a new category.",
    'delete_intro':  "Are you sure you want to delete category '%s'?",
    'edit_intro':  "Use this form to update this category.",
}
make_tag_messages = {
    'create_success':  "A new tag has been created.  Name: %s",
    'delete_success':  "The %s tag has been deleted.",
    'edit_success':  "The %s tag has been updated.",
    'create_intro':  "Use this form to create a new tag.",
    'delete_intro':  "Are you sure you want to delete tag '%s'?",
    'edit_intro':  "Use this form to update this tag.",
}
make_subitem_messages = {
    'create_success':  "A new subitem has been created.  Name: %s",
    'delete_success':  "The %s subitem has been deleted.",
    'edit_success':  "The %s subitem has been updated.",
    'create_intro':  "Use this form to create a new subitem.",
    'delete_intro':  "Are you sure you want to delete subitem '%s'?",
    'edit_intro':  "Use this form to update this subitem.",
}

delete_item_messages = {
    'delete_success':  "The %s item has been deleted.",
    'delete_intro':  "Are you sure you want to delete item '%s'?",
}
