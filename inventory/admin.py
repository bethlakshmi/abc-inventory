from django.contrib import admin
from inventory.models import *
from import_export.admin import ImportExportActionModelAdmin


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'name',
                    'help_text')
    list_editable = ('name', 'help_text')


class TagAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'name',
                    'help_text')
    list_editable = ('name', 'help_text')


class DispositionAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'state',
                    'help_text',)
    list_editable = ('state',
                     'help_text',)


class ItemTextInline(admin.TabularInline):
    model = ItemText
    extra = 1
    verbose_name_plural = "wall text"


class ItemImageInline(admin.TabularInline):
    model = ItemImage
    extra = 1


class SubitemInline(admin.TabularInline):
    model = Subitem
    extra = 1


class ItemAdmin(ImportExportActionModelAdmin):
    list_display = ('id',
                    'title',
                    'has_label',
                    'has_image',
                    'category',
                    'disposition',
                    'year',
                    'width',
                    'height',
                    'depth',
                    'subject',
                    'date_acquired',
                    'price',
                    'note')
    list_filter = ['category', 'disposition', 'tags', 'subject']
    search_fields = ['title',
                     'category__name',
                     'disposition__state',
                     'year',
                     'subject',
                     'date_acquired',
                     'price',
                     'note',
                     'price']

    inlines = [
        SubitemInline,
        ItemTextInline,
        ItemImageInline,
    ]

    filter_horizontal = ("connections", "tags")


class ItemImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'item', 'filer_image')


class ItemTextAdmin(admin.ModelAdmin):
    list_display = ('id', 'item', 'text')


class SubItemAdmin(ImportExportActionModelAdmin):
    list_display = ('id',
                    'subitem_number',
                    'title',
                    'item',
                    'width',
                    'height',
                    'depth')
    list_filter = ['item__category__name',
                   'item__disposition__state',
                   'item__subject']
    search_fields = ['title',
                     'subitem_number',
                     'description',
                     'item__title',
                     'item__year',
                     'item__subject',
                     'item__description',
                     'item__note',
                     ]


class MessageAdmin(admin.ModelAdmin):
    list_display = ('view',
                    'code',
                    'summary',
                    'description')
    list_editable = ('summary', 'description')
    readonly_fields = ('view', 'code')
    list_filter = ['view', 'code']

class StylePropertyAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'selector',
        'pseudo_class',
        'style_property',
        'value_type')
    list_editable = (
        'selector',
        'pseudo_class',
        'style_property',
        'value_type')
    list_filter = [
        'selector',
        'pseudo_class',
        'style_property']

class StyleValueAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'style_version',
        'style_property',
        'value')
    list_editable = ('value', )
    list_filter = [
        'style_version__name',
        'style_version__number',
        'style_property__selector',
        'style_property__pseudo_class',
        'style_property__style_property']

admin.site.register(UserMessage, MessageAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Disposition, DispositionAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Subitem, SubItemAdmin)
admin.site.register(ItemText, ItemTextAdmin)
admin.site.register(ItemImage, ItemImageAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(StyleValue, StyleValueAdmin)
admin.site.register(StyleProperty, StylePropertyAdmin)
admin.site.register(StyleVersion)
