from django.core.management import BaseCommand
from core.models import ImageLocation


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
                    Image.objects.filter(code=code).update(
                        geographic_prefix = prefix,
                        geographic_name = name,
                    )
                    print "Loaded geocode for %s" % code
