from bs4 import BeautifulSoup
from django.core.management import BaseCommand


class Command(BaseCommand):
    """
    Ingests NASA images. For science.
    """

    def handle(self, *files, **kwargs):
        for file in files:
            self.ingest_file(file)

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
            elif line.lower().startswith("country or geog"):
                details['geographic_name'] = line.split(":", 1)[1].strip()
            elif line.lower().startswith("features"):
                details['features'] = line.split(":", 1)[1].strip()
            elif line.lower().startswith("center point latitude"):
                latitude = float(line.split(":", 1)[1].split()[0].strip())
                longitude =float(line.split(":", 2)[2].split()[0].strip())
                details['center_point'] = (latitude, longitude)
            elif last.lower().startswith("camera tilt"):
                details['camera_tilt'] = line
            elif line.lower().startswith("camera focal length"):
                details['camera_focal_length'] = line.split(":", 1)[1].strip()
            elif last.lower().startswith("camera:"):
                details['camera_model_text'] = line
                details['camera_model_code'] = line.split(":")[0].strip()
            elif last.lower().startswith("film"):
                details['film_text'] = line
                details['film_text_code'] = line.split(":")[0].strip()
            elif line.lower().startswith("percentage of cloud cover"):
                details['cloud_cover'] = int(line.split(":", 1)[1].split()[0].strip())
            last = line
        # Data!
        print details
