from django.views.generic.base import TemplateView
from core.models import Image

class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context["images"] = Image.objects.order_by("-rating")[:12]
        return context
