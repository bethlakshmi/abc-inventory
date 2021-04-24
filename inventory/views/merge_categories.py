from inventory.views import GenericWizard
from inventory.forms import (
    ChooseCategoryForm,
    PickCategoryNameForm,
)
from django.contrib import messages
from django.urls import reverse
from inventory.models import (
    Category,
    Item,
)


class MergeCategories(GenericWizard):
    template = 'inventory/generic_wizard.tmpl'
    page_title = 'Merge Categories'
    first_title = 'Pick Categories to Merge'
    second_title = 'Select Category Name'
    form_sets = {
        -1: {
            'the_form':  None,
            'next_form': ChooseCategoryForm,
            'next_title': first_title},
        0: {
            'the_form':  ChooseCategoryForm,
            'next_form': PickCategoryNameForm,
            'next_title': second_title},
        1: {
            'the_form':  PickCategoryNameForm,
            'next_form': None,
            'next_title': None},
    }

    def groundwork(self, request, args, kwargs):
        self.step = int(request.POST.get("step", -1))
        self.return_url = reverse('categories_list', urlconf='inventory.urls')

    def finish_valid_form(self, request):
        if self.forms[0].__class__.__name__ == "ChooseCategoryForm":
            self.categories = self.forms[0].cleaned_data['categories']
            # Confirm category, category, ... into <chosen category selection>
            cat_list = "Confirm merge of categories: "
            for category in self.categories:
                cat_list = cat_list + category.name + ', '
            self.current_form_set['confirm_msg'] = (
                "'%s'+document.getElementById('id_category').options[" +
                "document.getElementById('id_category').selectedIndex].text" +
                "+'.'") % (" into ".join(cat_list.rsplit(", ", 1)))
        else:
            self.categories = self.forms[0].cleaned_data['categories']
            self.target_category = self.forms[0].cleaned_data['category']
            self.num_items = Item.objects.filter(
                category__in=self.categories.exclude(
                    pk=self.target_category.pk)).update(
                category=self.target_category)
            self.categories.exclude(pk=self.target_category.pk).delete()

    def finish(self, request):
        messages.success(
            request,
            "Merged %d categories, re-categorized %d items to %s." % (
                len(self.categories),
                self.num_items,
                self.target_category))
        return self.return_url

    def setup_forms(self, form, request=None):
        if request:
            if str(form().__class__.__name__) == "ChooseCategoryForm":
                return [form(request.POST)]
            else:
                pick_form = form(request.POST)
                pick_form.fields[
                    'category'].queryset = Category.objects.filter(
                        pk__in=request.POST.getlist("categories"))
                return [pick_form]
        else:
            if str(form().__class__.__name__) == "ChooseCategoryForm":
                return [form()]
            else:
                pick_form = form(initial={'categories': self.categories})
                pick_form.fields['category'].queryset = self.categories
                return [pick_form]
