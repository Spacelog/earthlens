from django.contrib.admin import site
from core.models import Mission, Image, ImageVote, Tag, UserTag, ImageLocation

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

site.register(
    Tag,
    list_display = ["id", "name", "slug"],
)

site.register(
    UserTag,
    list_display = ["id", "image", "user", "tagged"],
)

site.register(
    ImageLocation,
    list_display = ["image", "preposition", "location"],
)
