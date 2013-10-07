from django.views.generic import TemplateView, DetailView
from django.db.models import F
from django.http import HttpResponseRedirect, Http404
from core.models import Image, ImageVote


class IndexView(TemplateView):

    template_name = "index.html"
    row_pattern = [5, 4]
    page_size = 18

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        offset = int(self.request.GET.get("offset", 0))
        context["rows"] = self.make_rows(Image.objects.order_by("-rating", "-votes")[offset:offset+self.page_size])
        if not context["rows"][0]:
            raise Http404("No images left")
        context["page_size"] = self.page_size
        return context

    def make_rows(self, images):
        rows = [[]]
        for image in images:
            if len(rows[-1]) >= self.row_pattern[(len(rows) - 1) % len(self.row_pattern)]:
                rows.append([])
            rows[-1].append(image)
        return rows


class IndexAjaxView(IndexView):

    template_name = "_index_rows.html"


class ImageView(DetailView):

    template_name = "image.html"
    model = Image

    def post(self, request, pk, **kwargs):
        if "good" in self.request.POST:
            rating = 1
        elif "bad" in self.request.POST:
            rating = -1
        elif "awesome" in self.request.POST:
            rating = 3
        else:
            rating = 0

        try:
            vote = ImageVote.objects.get(user=request.user, image__pk=pk)
        except ImageVote.DoesNotExist:
            Image.objects.filter(pk=pk).update(
                rating = F("rating") + rating,
                votes = F("votes") + 1,
            )
            ImageVote.objects.create(user=request.user, image_id=pk, vote=rating)
        else:
            Image.objects.filter(pk=pk).update(
                rating = F("rating") + (rating - vote.vote),
            )

        return HttpResponseRedirect(self.request.POST.get("next", "."))


class RateView(TemplateView):

    template_name = "rate.html"

    def get_context_data(self):
        try:
            image = Image.objects.exclude(vote_objects__user=self.request.user).order_by("?")[0]
        except IndexError:
            return {"image": None}
        return {
            "image": image,
            "prev_image": Image.objects.get(pk=self.request.GET['prev']) if "prev" in self.request.GET else None,
        }
