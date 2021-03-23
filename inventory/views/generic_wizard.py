from django.views.generic import View
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from inventory.models import UserMessage
from inventory.views.default_view_text import user_messages
from django.shortcuts import render


class GenericWizard(View):
    ##############
    #  This is an abstract class, it gives the logic for rolling through
    #  a set of forms as a wizard, to use it:
    #     - instantiate form_sets = a dict of integers (-1 to however many)
    #          - with a sub-dict with a "the_form", "next_form", "next_title"
    #          - there must be a -1 with the_form = None
    #          - there must be a last item with next_form and next_title
    #            as None
    #     - create setup_forms - which can make any form in the set, the first
    #          form can be  made via either get or post, all forms after that
    #          are submitted as posts.
    #     - finish_valid_form - what to do when a form is deemed valid
    #     - finish - place to put any messaging and return a URL for how to
    #          return to a main spot
    #     - redirect (only used with add) - a place to redirect to continue
    ##############
    step = -1
    max = 1

    def groundwork(self, request, args, kwargs):
        self.step = int(request.POST.get("step", -1))
        self.return_url = reverse('items_list', urlconf='inventory.urls')

    def make_context(self, request):
        context = {
            'page_title': self.page_title,
            'title': self.page_title,
            'subtitle': self.current_form_set['next_title'],
            'forms': self.forms,
            'first': self.current_form_set['the_form'] is None,
            'last': self.form_sets[self.step+1]['next_form'] is None,
        }
        return context

    def make_back_forms(self, request):
        self.step = self.step - 2
        self.current_form_set = self.form_sets[self.step]

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(GenericWizard, self).dispatch(*args, **kwargs)

    @never_cache
    def get(self, request, *args, **kwargs):
        redirect = self.groundwork(request, args, kwargs)
        self.current_form_set = self.form_sets[-1]
        self.forms = self.setup_forms(self.current_form_set['next_form'])
        return render(request, self.template, self.make_context(request))

    def return_on_error(self, request, message_code, extra_message=""):
        msg = UserMessage.objects.get_or_create(
                view=self.__class__.__name__,
                code=message_code,
                defaults={
                    'summary': user_messages[message_code]['summary'],
                    'description': user_messages[message_code]['description']}
                )
        messages.error(request, msg[0].description + extra_message)
        return HttpResponseRedirect(self.return_url)

    @never_cache
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        self.groundwork(request, args, kwargs)
        if 'cancel' in list(request.POST.keys()):
            messages.success(request, "The last update was canceled.")
            return HttpResponseRedirect(self.return_url)

        if 'next' in list(request.POST.keys()) or 'finish' in list(
                request.POST.keys()) or 'add' in list(request.POST.keys()
                ) or 'redirect' in list(request.POST.keys()):
            all_valid = True
            self.current_form_set = self.form_sets[self.step]
            if not self.current_form_set['the_form']:
                return self.return_on_error(request, "STEP_ERROR")
            self.forms = self.setup_forms(
                self.current_form_set['the_form'],
                request)
            if len(self.forms) == 0:
                return self.return_on_error(request, "NO_FORM_ERROR")
            for form in self.forms:
                all_valid = form.is_valid() and all_valid
            if not all_valid:
                self.step = self.step - 1
                self.current_form_set = self.form_sets[self.step]
                return render(request, self.template, self.make_context(
                    request))
            self.finish_valid_form(request)
            if 'finish' in list(request.POST.keys()):
                return HttpResponseRedirect(self.finish(request))
            if 'add' in list(request.POST.keys()):
                self.step = self.step - 1
                self.current_form_set = self.form_sets[self.step]
            if 'redirect' in list(request.POST.keys()):
                return HttpResponseRedirect(self.redirect(request))

        elif 'back' in list(request.POST.keys()):
            self.make_back_forms(request)
        else:
            msg = UserMessage.objects.get_or_create(
                view=self.__class__.__name__,
                code="BUTTON_CLICK_UNKNOWN",
                defaults={
                    'summary': user_messages["BUTTON_CLICK_UNKNOWN"]
                    ['summary'],
                    'description': user_messages["BUTTON_CLICK_UNKNOWN"]
                    ['description']}
                )
            messages.error(request, msg[0].description)
            self.current_form_set = {'next_form': None}

        if self.current_form_set['next_form'] is not None:
            self.forms = self.setup_forms(self.current_form_set['next_form'])
            return render(request, self.template, self.make_context(request))

        return HttpResponseRedirect(self.return_url)
