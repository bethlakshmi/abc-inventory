from dal import autocomplete

from inventory.models import Color


class ColorAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Color.objects.none()

        qs = Color.objects.all()

        if self.q:
            qs = qs.filter(name__icontains=self.q)

        return qs
