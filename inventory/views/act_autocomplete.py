from dal import autocomplete
from inventory.models import Act


class ActAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Act.objects.none()

        qs = Act.objects.all()

        if self.q:
            qs = qs.filter(title__icontains=self.q)

        return qs
