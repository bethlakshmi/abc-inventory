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
from inventory.forms import StepForm


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
    # Optional stuff:
    #     - adding instruction_key to any form set will give that string as
    #          instructions at the top of the form (unless you use a special
    #          handling case, in which case this is your problem)
    #     - confirm_msg = if present, the submission of the form will trigger
    #          a confirmation window with this as the message.  This can be
    #          Javascript - so if you want to pull from the form data, have
    #          a blast.
    ##############
    step = -1
    max = 1

    def groundwork(self, request, args, kwargs):
        self.step = int(request.POST.get("step", -1))
        self.return_url = reverse('items_list', urlconf='inventory.urls')

    def make_context(self, request, valid=True):
        context = {
            'page_title': self.page_title,
            'title': self.page_title,
            'subtitle': self.current_form_set['next_title'],
            'forms': self.forms,
            'first': self.current_form_set['the_form'] is None,
            'show_finish': True,
            'last': self.form_sets[self.step+1]['next_form'] is None,
            'step_form': StepForm(initial={"step": self.step + 1})
        }
        if 'instruction_key' in self.current_form_set:
            context['instructions'] = UserMessage.objects.get_or_create(
                view=self.__class__.__name__,
                code=self.current_form_set['instruction_key'],
                defaults={
                    'summary': user_messages[self.current_form_set[
                        'instruction_key']]['summary'],
                    'description': user_messages[self.current_form_set[
                        'instruction_key']]['description']}
                )[0].description
        if 'confirm_msg' in self.current_form_set:
            context['confirm_msg'] = self.current_form_set['confirm_msg']
        context['form_error'] = not valid
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
        # so template is set before render - not critical on get
        context = self.make_context(request)
        return render(request, self.template, context)

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

    def validate_forms(self):
        all_valid = True
        for form in self.forms:
            all_valid = form.is_valid() and all_valid
        return all_valid

    @never_cache
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        self.groundwork(request, args, kwargs)
        if 'cancel' in list(request.POST.keys()):
            messages.success(request, "The last update was canceled.")
            return HttpResponseRedirect(self.return_url)

        if 'next' in list(request.POST.keys()) or 'finish' in list(
                request.POST.keys()) or 'add' in list(
                request.POST.keys()) or 'redirect' in list(
                request.POST.keys()):
            self.current_form_set = self.form_sets[self.step]
            if not self.current_form_set['the_form']:
                return self.return_on_error(request, "STEP_ERROR")
            self.forms = self.setup_forms(
                self.current_form_set['the_form'],
                request)
            if ("is_formset" not in self.current_form_set or (
                    not self.current_form_set['is_formset'])) and len(
                    self.forms) == 0:
                return self.return_on_error(request, "NO_FORM_ERROR")

            if not self.validate_forms():
                self.step = self.step - 1
                self.current_form_set = self.form_sets[self.step]
                # gets template set before render
                context = self.make_context(request, valid=False)
                return render(request, self.template, context)
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
            # gets template set before render
            context = self.make_context(request)
            return render(request, self.template, context)
        return HttpResponseRedirect(self.return_url)
