from dal import autocomplete
from inventory.models import Show


class ShowAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Show.objects.none()

        qs = Show.objects.all()

        if self.q:
            qs = qs.filter(title__icontains=self.q)

        return qs
