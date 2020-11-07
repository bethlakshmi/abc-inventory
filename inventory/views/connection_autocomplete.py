from dal import autocomplete
from django.db.models import Q
from inventory.models import Item


class ConnectionAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Item.objects.none()

        qs = Item.objects.all()

        if self.q:
            qs = qs.filter(
                Q(title__icontains=self.q) |
                Q(description__icontains=self.q) |
                Q(year__icontains=self.q) |
                Q(subject__icontains=self.q) |
                Q(note__icontains=self.q))

        return qs
