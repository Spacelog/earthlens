from django.core.management import BaseCommand
from core.models import ImageLocation, Image


class Command(BaseCommand):
    """
    Hides all but the best 1/2 images in each group.
    """

    def handle(self, file, **kwargs):
        with open(file) as fh:
            for line in fh:
                line = line.strip()
                if line:
                    code, prefix, name = line.split("\t")
                    image = Image.objects.get(code=code)
                    try:
                        location = ImageLocation.objects.get(image=image)
                    except ImageLocation.DoesNotExist:
                        location = ImageLocation(image=image)
                    location.preposition = prefix
                    location.location = name
                    location.save()
                    print "Loaded geocode for %s" % code
