from django.contrib.admin import site
from core.models import Mission, Image, ImageFile

site.register(
    Mission,
    list_display = ["code", "name"]
)

site.register(
    Image,
    list_display = ["id", "code", "mission"],
)

site.register(
    ImageFile,
    list_display = ["id", "file", "width", "height"],
)
