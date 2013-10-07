from django.views.generic import TemplateView
from core.models import Image

class IndexView(TemplateView):
    template_name = "index.html"

    def get_context(self):
        return {
            "images": Image.objects.order_by("-rating")[:12],
        }
