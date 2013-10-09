from django.core.management import BaseCommand
from core.models import Image, Mission


class Command(BaseCommand):
    """
    Hides all but the best 1/2 images in each group.
    """

    def handle(self, *files, **kwargs):
        # Loop through each mission
        for mission in Mission.objects.all():
            print "Mission %s" % mission.code
            run = []
            for image in Image.objects.filter(mission=mission).order_by("date", "code"):
                if image.in_group:
                    run.append(image)
                else:
                    if run:
                        self.mark_run(run)
                    run = []
            if run:
                self.mark_run(run)

    def mark_run(self, run):
        # Find the best-rated images
        run.sort(key=lambda i: i.rating, reverse=True)
        number_to_show = (len(run) // 5) + 1
        for i, image in enumerate(run):
            image.group_hides = (i >= number_to_show)
            image.save()
        print "Handled run of %s" % len(run)
