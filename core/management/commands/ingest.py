import datetime
import traceback
from bs4 import BeautifulSoup
from django.core.management import BaseCommand
from django.utils.termcolors import colorize
from core.models import Image, Mission


class Command(BaseCommand):
    """
    Ingests NASA images. For science.
    """

    def handle(self, *files, **kwargs):
        for file in files:
            try:
                self.ingest_file(file)
            except StandardError:
                traceback.print_exc()
                raise

    def ingest_file(self, file):
        # Soup that file
        with open(file) as fh:
            contents = fh.read()
        soup = BeautifulSoup(contents)
        text = soup.get_text()
        lines = text.split("\n")
        # Walk through lines getting data
        last = ""
        details = {'caption_text': None}
        missing = set()
        in_caption = False
        for line in lines:
            line = line.strip()
            if in_caption:
                if line.lower().startswith("download packaged file") or line.lower().startswith("no captions available"):
                    in_caption = False
                    details['caption_text'] = ((details['caption_text'] + "\n") if details['caption_text'] else None)
                elif line:
                    details['caption_text'] += line + "\n"
            elif last.lower().endswith("display record"):
                details['code'] = line.upper()
                details['mission'] = line.split("-")[0]
            elif line.lower().startswith("country or geog"):
                details['geographic_name'] = line.split(":", 1)[1].strip()
            elif line.lower().startswith("features"):
                details['features_text'] = line.split(":", 1)[1].strip()
            elif line.lower().startswith("center point latitude"):
                try:
                    details['latitude'] = float(line.split(":", 1)[1].split()[0].strip().strip(","))
                    details['longitude'] = float(line.split(":", 2)[2].split()[0].strip().strip(","))
                except ValueError:
                    missing.add("center")
            elif last.lower().startswith("camera tilt"):
                details['tilt_text'] = line
            elif line.lower().startswith("camera focal length"):
                details['focal_length_text'] = line.split(":", 1)[1].strip()
            elif last.lower().startswith("camera:"):
                details['camera_model_text'] = line
                details['camera_model_code'] = line.split(":")[0].strip()
            elif last.lower().startswith("film:"):
                details['film_text'] = line
                details['film_code'] = line.split(":")[0].strip()
            elif line.lower().startswith("percentage of cloud cover"):
                try:
                    details['cloud_cover_text'] = int(line.split(":", 1)[1].split()[0].strip())
                except ValueError:
                    missing.add("cloud_cover")
            elif line.lower().startswith("nadir point latitude"):
                try:
                    details['nadir_latitude'] = float(line.split(":", 1)[1].split()[0].strip().strip(","))
                    details['nadir_longitude'] = float(line.split(":", 2)[2].split()[0].strip().strip(","))
                except ValueError:
                    missing.add("nadir")
            elif last.lower().startswith("nadir to photo"):
                details['nadir_to_photo_text'] = line
            elif line.lower().startswith("sun azimuth"):
                try:
                    details['sun_azimuth'] = int(line.split(":", 1)[1].split()[0].strip())
                except ValueError:
                    missing.add("sun_azimuth")
            elif line.lower().startswith("sun elevation angle"):
                try:
                    details['sun_elevation'] = int(line.split(":", 1)[1].split()[0].strip())
                except ValueError:
                    missing.add("sun_elevation")
            elif line.lower().startswith("spacecraft altitude"):
                try:
                    details['altitude'] = int(line.split(":", 1)[1].split()[0].strip()) * 1852
                except ValueError:
                    missing.add("altitude")
            elif line.lower().startswith("gmt date"):
                details['date_text'] = line
                date_string = line.split(":")[1].split()[0].strip()
                time_string = line.split(":")[2].split()[0].strip()
                if date_string.endswith("____"):
                    try:
                        details['date'] = datetime.datetime(date_string[:4], 1, 1)
                        details['date_start'] = datetime.datetime(date_string[:4], 1, 1)
                        details['date_end'] = datetime.datetime(date_string[:4], 12, 31)
                    except (ValueError, TypeError):
                        missing.add("date")
                elif time_string.startswith("(HH"):
                    try:
                        details['date'] = datetime.datetime.strptime(date_string, "%Y%m%d")
                        details['date_start'] = details['date']
                        details['date_end'] = details['date'] + details['date'].replace(hour=23, minute=59, second=59)
                    except (ValueError, TypeError):
                        missing.add("date")
                else:
                    try:
                        details['date'] = datetime.datetime.strptime(date_string + "-" + time_string, "%Y%m%d-%H%M%S")
                    except (ValueError, TypeError):
                        missing.add("date")
            elif line.lower().startswith("captions"):
                in_caption = True
                details['caption_text'] = ""
            last = line
        # Make the models
        if "mission" not in details:
            print colorize("No mission in file %s" % file, fg="red")
            return
        mission = Mission.objects.get_or_create(code=details['mission'])[0]
        del details['mission']
        image, new = Image.objects.get_or_create(code=details['code'], mission=mission)
        for key, value in details.items():
            setattr(image, key, value)
        image.save()
        if new:
            print colorize("Ingested new image %s" % image, fg="green")
        else:
            print colorize("Updated existing image %s" % image, fg="cyan")
        if missing:
            print colorize("Image was missing: %s" % (", ".join(missing)))
