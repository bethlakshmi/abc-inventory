from dal import autocomplete
from inventory.models import Performer


class PerformerAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Performer.objects.none()

        qs = Performer.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs
