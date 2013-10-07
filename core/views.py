from django.views.generic import TemplateView, DetailView
from django.db.models import F
from django.http import HttpResponseRedirect
from core.models import Image

class IndexView(TemplateView):

    template_name = "index.html"
    row_pattern = [5, 4]

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context["rows"] = self.make_rows(Image.objects.order_by("-rating")[:14])
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
        Image.objects.filter(pk=pk).update(rating=F("rating") + rating)
        return HttpResponseRedirect(self.request.POST.get("next", "."))


class RateView(TemplateView):

    template_name = "rate.html"

    def get_context_data(self):
        return {
            "image": Image.objects.filter(rating=0).order_by("?")[0],
        }
