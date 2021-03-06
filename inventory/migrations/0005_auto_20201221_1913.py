# Generated by Django 2.2.17 on 2020-12-21 19:13

from django.db import migrations

init_values = [
    {
            'selector': '.bootstrap-table.fullscreen',
            'pseudo_class': '',
            'description': 'The table, when expanded to full screen',
            'target_element': 'div',
            'usage': 'Big Table',
            'prop_val': [('background-color', 'rgba(255,255,255,1)')]},
    {
            'selector': '#inventory-navbar-brand',
            'pseudo_class': '',
            'description': 'The site name at the upper left of the navbar',
            'target_element': 'a',
            'usage': 'Navbar',
            'prop_val': [('color', 'rgba(0,0,0,1)')]},
    {
            'selector': '.input-group-text:hover, .btn-inventory-secondary',
            'pseudo_class': 'hover',
            'description': 'Any active, but less important button, on hover',
            'target_element': 'button',
            'usage': 'Big Table',
            'prop_val': [('background-color', 'rgba(90,98,104,1)'),
                         ('border-color', 'rgba(90,98,104,1)'),
                         ('color', 'rgba(255,255,255,1)')]},
    {
            'selector': '.input-group-text, .btn-inventory-secondary',
            'pseudo_class': '',
            'description': 'Right now - the buttons above the table.',
            'target_element': 'button',
            'usage': 'Big Table',
            'prop_val': [('background-color', 'rgba(108,117,125,1)'),
                         ('border-color', 'rgba(108,117,125,1)'),
                         ('color', 'rgba(255,255,255,1)')]},
    {
            'selector': '.form-control:focus, .btn.focus, .btn:focus',
            'pseudo_class': '',
            'description': 'Right now - the buttons above the table.',
            'target_element': 'button',
            'usage': 'Big Table',
            'prop_val': [('box-shadow',
                          'px px px px rgba',
                          '0px 0px 0px 3px rgba(0,123,255,0.25)')]},
    {
            'selector': '.detail-icon',
            'pseudo_class': '',
            'description': 'The + sign on a table',
            'target_element': 'a',
            'usage': 'Big Table',
            'prop_val': [('color', 'rgba(0,123,255,1)')]},
    {
            'selector': '.detail-icon',
            'pseudo_class': 'hover',
            'description': 'The + sign on a table, on hover',
            'target_element': 'a',
            'usage': 'Big Table',
            'prop_val': [('color', 'rgba(0,86,179,1)')]},
    {
            'selector': '.inventory-detail',
            'pseudo_class': '',
            'description': 'The action icons on a table',
            'target_element': 'a',
            'usage': 'Big Table',
            'prop_val': [('color', 'rgba(0,123,255,1)')]},
    {
            'selector': '.inventory-detail',
            'pseudo_class': 'hover',
            'description': 'The action icons on a table, on hover',
            'target_element': 'a',
            'usage': 'Big Table',
            'prop_val': [('color', 'rgba(0,86,179,1)')]},
    {
            'selector': '.dropdown-menu',
            'pseudo_class': '',
            'description': 'The background of the table dropdown menu',
            'target_element': 'div',
            'usage': 'Navbar',
            'prop_val': [('background-color', 'rgba(255,255,255,1)')]},
    {
            'selector': '.inventory-alert-danger',
            'pseudo_class': '',
            'description': 'Alerts that show up dynamically on Error',
            'target_element': 'div',
            'usage': 'Alerts',
            'prop_val': [('background-color', 'rgba(248,215,218,1)'),
                         ('border-color', 'rgba(245,198,203,1)'),
                         ('color', 'rgba(114,28,36,1)')]},
    {
            'selector': '.inventory-alert-info',
            'pseudo_class': '',
            'description': 'Alerts that show up dynamically as Information',
            'target_element': 'div',
            'usage': 'Alerts',
            'prop_val': [('background-color', 'rgba(209,236,241,1)'),
                         ('border-color', 'rgba(190,229,235,1)'),
                         ('color', 'rgba(12,84,96,1)')]},
    {
            'selector': '.inventory-alert-success',
            'pseudo_class': '',
            'description': 'Alerts that show up dynamically on Success',
            'target_element': 'div',
            'usage': 'Alerts',
            'prop_val': [('background-color', 'rgba(212,237,218,1)'),
                         ('border-color', 'rgba(195,230,203,1)'),
                         ('color', 'rgba(21,87,36,1)')]},
    {
            'selector': '.inventory-alert-warning',
            'pseudo_class': '',
            'description': 'Alerts that show up dynamically on Warning',
            'target_element': 'div',
            'usage': 'Alerts',
            'prop_val': [('background-color', 'rgba(255,243,205,1)'),
                         ('border-color', 'rgba(255,238,186,1)'),
                         ('color', 'rgba(133,100,4,1)')]},
    {
            'selector': 'span.dropt:hover span',
            'pseudo_class': 'hover',
            'description': 'The help text hover',
            'target_element': 'span',
            'usage': 'Forms',
            'prop_val': [('background', 'rgba(255,255,255,1)')]},
    {
            'selector': 'span.dropt span',
            'pseudo_class': 'hover',
            'description': 'The help text hover',
            'target_element': 'span',
            'usage': 'Forms',
            'prop_val': [('border-color', 'rgba(0,0,0,1)')]},
    {
            'selector': '.inventory-btn-light',
            'pseudo_class': 'hover',
            'description': 'Hover for buttons that terminate the work',
            'target_element': 'input',
            'usage': 'Forms',
            'prop_val': [('background-color', 'rgba(226,230,234,1)'),
                         ('border-color', 'rgba(226,230,234,1)'),
                         ('color', 'rgba(33,37,41,1)')]},
    {
            'selector': '.inventory-btn-light',
            'pseudo_class': '',
            'description': 'Buttons like cancel that interrupt work.',
            'target_element': 'input',
            'usage': 'Forms',
            'prop_val': [('background-color', 'rgba(248,249,250,1)'),
                         ('border-color', 'rgba(248,249,250,1)'),
                         ('color', 'rgba(33,37,41,1)')]},
    {
            'selector': '.inventory-btn-primary',
            'pseudo_class': 'hover',
            'description': 'Hover for main buttons.',
            'target_element': 'input',
            'usage': 'Forms',
            'prop_val': [('background-color', 'rgba(0,105,217,1)'),
                         ('border-color', 'rgba(0,98,204,1)'),
                         ('color', 'rgba(255,255,255,1)')]},
    {
            'selector': '.inventory-btn-primary',
            'pseudo_class': '',
            'description': 'Buttons do the main work flow.',
            'target_element': 'input',
            'usage': 'Forms',
            'prop_val': [('background-color', 'rgba(0,123,255,1)'),
                         ('border-color', 'rgba(0,123,255,1)'),
                         ('color', 'rgba(255,255,255,1)')]},
    {
            'selector': '.inventory-form-error',
            'pseudo_class': '',
            'description': 'Text that informs user of a form error.',
            'target_element': 'font',
            'usage': 'Forms',
            'prop_val': [('color', 'rgb(255,0,0,1)')]},
    {
            'selector': '.inventory-form-required',
            'pseudo_class': '',
            'description': 'The * on required form fields',
            'target_element': 'font',
            'usage': 'Forms',
            'prop_val': [('color', 'rgb(255,0,0,1)')]},
    {
            'selector': '.inventory-nav-link',
            'pseudo_class': 'hover',
            'description': 'Items in drop down menus on hover.',
            'target_element': 'font',
            'usage': 'Navbar',
            'prop_val': [('color', 'rgba(0,0,0,.7)')]},
    {
            'selector': '.inventory-nav-link',
            'pseudo_class': '',
            'description': 'Items in drop down menu made with Django CMS',
            'target_element': 'font',
            'usage': 'Navbar',
            'prop_val': [('color', 'rgba(0,0,0,.5)')]},
    {
            'selector': '.inventory-title',
            'pseudo_class': '',
            'description': 'Biggest Header on the page',
            'target_element': 'h2',
            'usage': 'General',
            'prop_val': [
                ('color', 'rgba(0,0,0,1)'),
                ('text-shadow',
                 'px px px rgba',
                 '5px 5px 5px rgba(10,255,255,1)')]
    },
    {
            'selector': '.inventory-subtitle',
            'pseudo_class': '',
            'description': 'Second Biggest Header on the page',
            'target_element': 'h3',
            'usage': 'General',
            'prop_val': [('color', 'rgb(128,128,128,1)')]},
    {
            'selector': 'body.full-page',
            'pseudo_class': '',
            'description': '''Body of the page, but only for things like
            whole page tables''',
            'target_element': 'div',
            'usage': 'Big Table',
            'prop_val': [('background-color', 'rgba(255,255,255,1)'),
                         ('color', 'rgba(0,0,0,1)'),
                         ('background-image', 'image', '')]},
    {
            'selector': 'body.with-margin',
            'pseudo_class': '',
            'description': 'Body of the page, for any page with margins',
            'target_element': 'div',
            'usage': 'General',
            'prop_val': [('background-color', 'rgba(255,255,255,1)'),
                         ('color', 'rgba(0,0,0,1)'),
                         ('background-image', 'image', '')]},
    {
            'selector': '.inventory-table-header',
            'pseudo_class': '',
            'description': 'Table headers',
            'target_element': 'div',
            'usage': 'Big Table',
            'prop_val': [('background-color', 'rgba(245,245,245,1)'),
                         ('color', 'rgba(0,0,0,1)')]},
    {
            'selector': '.inventory-table-success',
            'pseudo_class': '',
            'description': 'Table row when it was just successfully updated',
            'target_element': 'div',
            'usage': 'Big Table',
            'prop_val': [('background-color', 'rgba(195,230,203,1)')]},
    {
            'selector': '.inventory-table-error',
            'pseudo_class': '',
            'description': 'Table row when it was just successfully updated',
            'target_element': 'div',
            'usage': 'Big Table',
            'prop_val': [('background-color', 'rgba(248,215,218,1)')]},
    {
            'selector': 'table.table-hover tbody tr.inventory-table-success',
            'pseudo_class': 'hover',
            'description': 'Table row when it was just successfully updated',
            'target_element': 'div',
            'usage': 'Big Table',
            'prop_val': [('background-color', 'rgba(156,184,162,1)')]},
    {
            'selector': 'table.table-hover tbody tr.inventory-table-error',
            'pseudo_class': 'hover',
            'description': 'Table row when it was just successfully updated',
            'target_element': 'div',
            'usage': 'Big Table',
            'prop_val': [('background-color', 'rgba(219,191,191,1)')]},
    {
            'selector': '.inventory-text-success',
            'pseudo_class': '',
            'description': '''Text that means to show success,like icons for
            something that is live.''',
            'target_element': 'div',
            'usage': 'Big Table',
            'prop_val': [('color', 'rgba(35,145,60,1)')]},
    {
            'selector': '.inventory-text-muted',
            'pseudo_class': '',
            'description': '''Text that is possibly active,but muted to
            defer so something else.''',
            'target_element': 'div',
            'usage': 'Big Table',
            'prop_val': [('color', 'rgba(108,117,125,1)')]},
    {
            'selector': '.inventory-table > thead > tr > th',
            'pseudo_class': '',
            'description': 'Table - header cell borders',
            'target_element': 'div',
            'usage': 'Big Table',
            'prop_val': [('border-color', 'rgb(128,128,128,1)')]},
    {
            'selector': '.inventory-table > tbody > tr > td',
            'pseudo_class': '',
            'description': 'Table - body cell borders',
            'target_element': 'div',
            'usage': 'Big Table',
            'prop_val': [('border-color', 'rgb(128,128,128,1)')]},
    ]


def initialize_style(apps, schema_editor):
    # We get the model from the versioned app registry;
    # if we directly import it, it'll be the wrong version
    StyleVersion = apps.get_model("inventory", "StyleVersion")
    StyleSelector = apps.get_model("inventory", "StyleSelector")
    StyleProperty = apps.get_model("inventory", "StyleProperty")
    StyleValue = apps.get_model("inventory", "StyleValue")
    version = StyleVersion(
        name="Baseline",
        number=1.0,
        currently_live=True,
        currently_test=True)
    version.save()

    for select_val in init_values:
        selector = StyleSelector(
            selector=select_val['selector'],
            description=select_val['description'],
            pseudo_class=select_val['pseudo_class'],
            used_for=select_val['usage'])
        selector.save()
        for prop_val in select_val['prop_val']:
            val = prop_val[1]
            if len(prop_val) == 2:
                style_prop = StyleProperty(
                    selector=selector,
                    style_property=prop_val[0],
                    value_type='rgba')
            elif len(prop_val) == 3:
                style_prop = StyleProperty(
                    selector=selector,
                    style_property=prop_val[0],
                    value_type=prop_val[1])
                val = prop_val[2]
            else:
                raise Exception("there should be 2 or 3 values here")
            style_prop.save()
            value = StyleValue(style_property=style_prop,
                               style_version=version,
                               value=val)
            value.save()


def destroy_style(apps, schema_editor):
    StyleVersion = apps.get_model("inventory", "StyleVersion")
    StyleSelector = apps.get_model("inventory", "StyleSelector")
    StyleVersion.objects.filter(name="Baseline", number=1.0).delete()
    for select_val in init_values:
        StyleSelector.objects.filter(
            selector=select_val['selector'],
            pseudo_class=select_val['pseudo_class']).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0004_auto_20210126_1859'),
    ]

    operations = [
        migrations.RunPython(initialize_style, reverse_code=destroy_style),
    ]
