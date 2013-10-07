from django.db import models


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

    def __str__(self):
        return "%s-%s" % (self.mission.code, self.code)

    def get_url(self, size="original"):
        return "/static/missions/%s/%s/%s.jpg" % (self.mission.code, size, self.code)

    def get_square_url(self):
        return self.get_url("square")

    def get_original_url(self):
        return self.get_url("original")

    def get_large_url(self):
        return self.get_url("large")


class ImageFile(models.Model):
    """
    A particular file and size of an image
    """

    image = models.ForeignKey(Image)
    file = models.FileField(upload_to="image_files")
    width = models.IntegerField()
    height = models.IntegerField()

    def __str__(self):
        return "%s (%sx%s)" % (self.file, self.width, self.height)
