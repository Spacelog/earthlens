from django.contrib.admin import site
from core.models import Mission, Image, ImageVote

site.register(
    Mission,
    list_display = ["code", "name"]
)

site.register(
    Image,
    list_display = ["id", "code", "mission"],
)

site.register(
    ImageVote,
    list_display = ["id", "image", "user", "vote"],
)
