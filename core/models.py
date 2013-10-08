from django.db import models
from django.conf import settings


class Mission(models.Model):
    """
    A mission on which photos were taken.
    """

    code = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return "%s (%s)" % (self.name, self.code)


class Image(models.Model):
    """
    An image from SPAAAACE.
    """

    mission = models.ForeignKey(Mission)
    code = models.CharField(max_length=30, unique=True)

    latitude = models.FloatField(null=True, blank=True, db_index=True)
    longitude = models.FloatField(null=True, blank=True, db_index=True)

    date = models.DateTimeField(null=True, blank=True, db_index=True)
    date_start = models.DateTimeField(null=True, blank=True)
    date_end = models.DateTimeField(null=True, blank=True)

    geographic_name = models.TextField(null=True, blank=True)
    features_text = models.TextField(null=True, blank=True)
    tilt_text = models.TextField(null=True, blank=True)
    focal_length_text = models.TextField(null=True, blank=True)
    camera_model_text = models.TextField(null=True, blank=True)
    camera_model_code = models.TextField(null=True, blank=True, db_index=True)
    film_text = models.TextField(null=True, blank=True)
    film_code = models.TextField(null=True, blank=True, db_index=True)
    exposure_text = models.TextField(null=True, blank=True)
    cloud_cover_text = models.TextField(null=True, blank=True)
    date_text = models.TextField(null=True, blank=True)
    caption_text = models.TextField(null=True, blank=True)

    nadir_latitude = models.FloatField(null=True, blank=True)
    nadir_longitude = models.FloatField(null=True, blank=True)
    nadir_to_photo_text = models.TextField(null=True, blank=True)
    sun_azimuth = models.IntegerField(null=True, blank=True)  # Degrees
    sun_elevation = models.IntegerField(null=True, blank=True)  # Degrees
    altitude = models.IntegerField(null=True, blank=True)  # In metres

    rating = models.IntegerField(default=0, db_index=True)
    votes = models.IntegerField(default=0, db_index=True)

    def __str__(self):
        return self.code

    def get_absolute_url(self):
        return "/image/%s/" % self.pk

    def get_image_url(self, size="original"):
        return "%s%s/%s/%s.jpg" % (settings.IMAGE_BASE_URL, self.mission.code, size, self.code)

    def get_square_url(self):
        return self.get_image_url("square")

    def get_original_url(self):
        return self.get_image_url("original")

    def get_large_url(self):
        return self.get_image_url("large")

    def get_descriptive_date(self):
        if self.date_start and self.date_end:
            return "%s to %s" % (self.date_start, self.date_end)
        elif self.date is not None:
            return self.date
        else:
            return None


class ImageVote(models.Model):
    """
    Stores a user's vote against an image.
    """

    user = models.ForeignKey("auth.User", related_name="vote_objects")
    image = models.ForeignKey(Image, related_name="vote_objects")
    vote = models.IntegerField()

    class Meta:
        unique_together = [
            ["user", "image"],
        ]


class Tag(models.Model):
    """
    Classification of an image.
    """

    name = models.TextField()
    slug = models.SlugField(unique=True)
    descriptive_image = models.ForeignKey(Image, null=True)


class UserTag(models.Model):
    """
    Stores a user's tag of an image.
    """

    user = models.ForeignKey("auth.User", related_name="tag_objects")
    image = models.ForeignKey(Image, related_name="tag_objects")
    tagged = models.ForeignKey(Tag)

