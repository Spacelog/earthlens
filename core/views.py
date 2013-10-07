from django.views.generic import TemplateView, DetailView
from django.db.models import F
from django.http import HttpResponseRedirect
from core.models import Image

class IndexView(TemplateView):

    template_name = "index.html"
    row_pattern = [5, 4]

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context["rows"] = self.make_rows(Image.objects.filter(mission__code="SL2").order_by("-rating")[:14])
        return context

    def make_rows(self, images):
        rows = [[]]
        for image in images:
            if len(rows[-1]) >= self.row_pattern[(len(rows) - 1) % len(self.row_pattern)]:
                rows.append([])
            rows[-1].append(image)
        return rows


class ImageView(DetailView):

    template_name = "image.html"
    model = Image

    def post(self, request, pk, **kwargs):
        if "good" in self.request.POST:
            rating = 1
        elif "bad" in self.request.POST:
            rating = -1
        else:
            rating = 0
        Image.objects.filter(pk=pk).update(
            rating=F("rating") + rating,
            votes=F("votes") + 1,
        )
        return HttpResponseRedirect(self.request.POST.get("next", "."))


class RateView(TemplateView):

    template_name = "rate.html"

    def get_context_data(self):
        return {
            "image": Image.objects.extra(where=["votes = (select min(votes) from core_image)"]).order_by("?")[0],
            "prev_image": Image.objects.get(pk=self.request.GET['prev']) if "prev" in self.request.GET else None,
        }
