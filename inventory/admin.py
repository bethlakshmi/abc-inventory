from django.contrib import admin
from inventory.models import *
from import_export.admin import ImportExportActionModelAdmin


class CategoryAdmin(admin.ModelAdmin):
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

class ItemImageInline(admin.TabularInline):
    model = ItemImage


class ItemAdmin(ImportExportActionModelAdmin):
    list_display = ('id',
                    'title',
                    'has_label',
                    'has_image',
                    'category',
                    'disposition',
                    'year',
                    'dimensions',
                    'subject',
                    'date_acquired',
                    'price',
                    'note',
                    'display_note')
    list_filter = ['category', 'disposition', 'subject']
    search_fields = ['title',
                     'category__name',
                     'disposition__state',
                     'year',
                     'subject',
                     'date_acquired',
                     'price',
                     'note',
                     'display_note',
                     'price']

    inlines = [
        ItemTextInline,
        ItemImageInline,
    ]

    def dimensions(self, obj):
        dimensions = "0w"
        if obj.width:
        	dimensions = "%dw" % obj.width
        if obj.height:
            dimensions += " x %dh" % obj.height
        if obj.depth:
            dimensions += " x %dd" % obj.depth
        return str(dimensions)

    def has_label(self, obj):
        return (obj.labels.count() > 0)

    def has_image(self, obj):
        return (obj.images.count() > 0)

class ItemImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'item')

class ItemTextAdmin(admin.ModelAdmin):
    list_display = ('id', 'item', 'text')

admin.site.register(Category, CategoryAdmin)
admin.site.register(Disposition, DispositionAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(ItemText, ItemTextAdmin)
admin.site.register(ItemImage, ItemImageAdmin)
