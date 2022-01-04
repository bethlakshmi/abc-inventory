from inventory.views import GenericWizard
from inventory.forms import (
    ItemRelatedData,
    ItemUploadForm,
    ItemUploadMapping,
    ItemUploadRow,
)
from inventory.models import Item
from django.contrib import messages
from django.forms import modelformset_factory
from django.conf import settings


class BulkItemUpload(GenericWizard):
    uploaded_items = []
    template = 'inventory/bulk_item_wizard.tmpl'
    page_title = 'Item Inventory Upload'
    first_title = 'Select File of Items'
    second_title = 'Preview Item Upload & Select Column Mapping'
    third_title = 'Add Additional Item Details'
    form_sets = {
        -1: {
            'the_form':  None,
            'next_form': ItemUploadForm,
            'next_title': first_title,
            'instruction_key': "BULK_FILE_UPLOAD_INSTRUCTIONS"},
        0: {
            'the_form':  ItemUploadForm,
            'next_form': ItemUploadMapping,
            'next_title': second_title,
            'instruction_key': "SETUP_ITEM_UPLOAD_INSTRUCTIONS"},
        1: {
            'the_form':  ItemUploadMapping,
            'next_form': None,
            'next_title': third_title,
            'instruction_key': "ADDITIONAL_ITEM_DETAIL_INSTRUCTIONS"},
    }
    header = None
    form_error = False

    def groundwork(self, request, args, kwargs):
        if settings.INVENTORY_MODE == "troupe":
            self.form_sets[1]['next_form'] = ItemRelatedData
            self.form_sets[2] = {'the_form': ItemRelatedData,
                                 'is_formset': True,
                                 'next_form': None,
                                 'next_title': None,
                                 }

        return super(BulkItemUpload, self).groundwork(
            request,
            args,
            kwargs)

    def validate_forms(self):
        if self.forms[0].__class__.__name__ == "ItemUploadForm" and super(
                BulkItemUpload, self).validate_forms():
            (self.num_cols,
             self.header,
             self.csv_data) = self.forms[0].check_and_get_data()
            if self.num_cols > 0 and self.csv_data is not None:
                self.num_rows = len(self.csv_data)
                return True
        elif self.forms[0].__class__.__name__ == "ItemUploadMapping":
            all_valid = True
            self.new_items = []
            translator = {}
            i = 0
            if not self.forms[0].is_valid():
                self.form_error = True
                return False

            while i < self.forms[0].cleaned_data['num_cols']:
                if len(self.forms[0].cleaned_data['header_%d' % i]) > 0:
                    translator[self.forms[0].cleaned_data[
                        'header_%d' % i]] = "cell_%d" % i
                i = i + 1
            for item_form in self.forms[1:]:
                formatted_data = item_form.validate_and_format(translator)
                if formatted_data:
                    self.new_items += [formatted_data]
                else:
                    self.form_error = True
                    all_valid = False
            return all_valid
        elif "is_formset" in self.current_form_set and self.current_form_set[
                'is_formset']:
            all_valid = self.forms.is_valid()
            return all_valid

    def finish_valid_form(self, request):
        if self.forms[0].__class__.__name__ == "ItemUploadMapping":
            # use the selection of mappings to build a bulk create
            # do the create
            self.uploaded_items = Item.objects.bulk_create(
                [Item(**kv) for kv in self.new_items])
            self.num_rows = len(self.new_items)
        elif "is_formset" in self.current_form_set and self.current_form_set[
                'is_formset']:
            self.forms.save()
            self.num_rows = self.forms.total_form_count()

    def finish(self, request):
        messages.success(
            request,
            "Uploaded %s items." % (
                self.num_rows))
        return self.return_url

    def make_context(self, request, valid=True):
        context = super(BulkItemUpload, self).make_context(request, valid)
        if str(self.forms[0].__class__.__name__) == "ItemUploadMapping":
            context['special_handling'] = True
            context['form_error'] = self.form_error
        elif str(self.forms[0].__class__.__name__) == "ItemUploadForm":
            context['show_finish'] = False
        elif str(self.forms.__class__.__name__) == "ItemFormFormSet":
            context['special_handling'] = True
            self.template = 'inventory/bulk_item_wizard2.tmpl'
            context['no_margin'] = True
        if self.header:
            context['header'] = self.header

        return context

    def setup_forms(self, form, request=None):
        if request:
            if str(form().__class__.__name__) == "ItemUploadForm":
                return [form(request.POST, request.FILES)]
            elif str(form().__class__.__name__) == "ItemUploadMapping":
                # set up the choice form based on number of columns.
                if 'num_cols' not in request.POST.keys() or (
                        'num_rows' not in request.POST.keys()):
                    return []
                num_cols = int(request.POST['num_cols'])
                num_rows = int(request.POST['num_rows'])
                forms = [ItemUploadMapping(request.POST,
                                           initial={'num_cols': num_cols})]
                i = 0
                while i < num_rows:
                    forms += [ItemUploadRow(request.POST,
                                            num_cols=num_cols,
                                            prefix=str(i))]
                    i = i + 1
                return forms
            else:
                ItemDetailFormSet = modelformset_factory(Item,
                                                         form=ItemRelatedData,
                                                         extra=0)
                forms = ItemDetailFormSet(request.POST)
                return forms
        else:
            if str(form().__class__.__name__) == "ItemUploadForm":
                return [form()]
            elif str(form().__class__.__name__) == "ItemUploadMapping":
                # set up the choice form based on number of columns.
                forms = [ItemUploadMapping(initial={
                    'num_cols': self.num_cols,
                    'num_rows': self.num_rows})]
                i = 0
                for row in self.csv_data:
                    forms += [ItemUploadRow(row=row, prefix=str(i))]
                    i = i + 1
                return forms
            else:
                ItemDetailFormSet = modelformset_factory(Item,
                                                         form=ItemRelatedData,
                                                         extra=0)
                item_ids = []
                for item in self.uploaded_items:
                    item_ids += [item.pk]
                forms = ItemDetailFormSet(
                    queryset=Item.objects.filter(pk__in=item_ids))
                return forms
