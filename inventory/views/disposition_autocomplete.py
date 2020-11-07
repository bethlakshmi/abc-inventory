from dal import autocomplete
from inventory.models import Disposition


class DispositionAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Disposition.objects.none()

        qs = Disposition.objects.all()

        if self.q:
            qs = qs.filter(state__istartswith=self.q)

        return qs
