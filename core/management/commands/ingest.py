import datetime
import traceback
from bs4 import BeautifulSoup
from django.core.management import BaseCommand
from core.models import Image, Mission


class Command(BaseCommand):
    """
    Ingests NASA images. For science.
    """

    def handle(self, *files, **kwargs):
        for file in files:
            try:
                self.ingest_file(file)
            except:
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
        details = {}
        for line in lines:
            line = line.strip()
            if last.lower().endswith("display record"):
                details['code'] = line
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
                    print "something funky in lat long that is not a number"
                    pass
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
                details['cloud_cover_text'] = int(line.split(":", 1)[1].split()[0].strip())
            elif line.lower().startswith("nadir point latitude"):
                try:
                    details['nadir_latitude'] = float(line.split(":", 1)[1].split()[0].strip().strip(","))
                    details['nadir_longitude'] = float(line.split(":", 2)[2].split()[0].strip().strip(","))
                except ValueError:
                    print 'nadir data is funked'
                    pass
            elif last.lower().startswith("nadir to photo"):
                details['nadir_to_photo_text'] = line
            elif line.lower().startswith("sun azimuth"):
                try:
                    details['sun_azimuth'] = int(line.split(":", 1)[1].split()[0].strip())
                except ValueError:
                    print 'sun azimuth is whack'
                    pass
            elif line.lower().startswith("sun elevation angle"):
                try:
                    details['sun_elevation'] = int(line.split(":", 1)[1].split()[0].strip())
                except ValueError:
                    print 'the sun has elevated out of a sensible value'
                    pass
            elif line.lower().startswith("spacecraft altitude"):
                try:
                    details['altitude'] = int(line.split(":", 1)[1].split()[0].strip()) * 1852
                except ValueError:
                    print 'altitude alti-wat'
                    pass
            elif line.lower().startswith("gmt date"):
                details['date_text'] = line
                date_string = line.split(":")[1].split()[0].strip()
                time_string = line.split(":")[2].split()[0].strip()
                if date_string.endswith("____"):
                    try:
                        details['date'] = datetime.datetime(date_string[:4], 1, 1)
                        details['date_start'] = datetime.datetime(date_string[:4], 1, 1)
                        details['date_end'] = datetime.datetime(date_string[:4], 12, 31)
                    except TypeError:
                        print 'date is funked up'
                        pass
                elif time_string.startswith("(HH"):
                    try:
                        details['date'] = datetime.datetime.strptime(date_string, "%Y%m%d")
                        details['date_start'] = details['date']
                        details['date_end'] = details['date'] + details['date'].replace(hour=23, minute=59, second=59)
                    except TypeError:
                        print 'date is funked up'
                        pass
                else:
                    details['date'] = datetime.datetime.strptime(date_string + "-" + time_string, "%Y%m%d-%H%M%S")
            last = line
        # Make the models
        mission = Mission.objects.get_or_create(code=details['mission'])[0]
        details['mission'] = mission
        image = Image.objects.get_or_create(**details)
        print image
