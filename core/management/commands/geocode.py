import traceback
from time import time, sleep
import requests
import lxml.etree
from pycountry import countries
from django.core.management import BaseCommand
from core.models import Image, ImageLocation

# Rate limit - seconds/request
RATE = 7.3  # 7.3 secs between hits for continuous use as per http://www.geonames.org/export/credits.html
ENDPOINT = 'http://api.geonames.org'
USERNAME = 'russss'

ADM1_COUNTRIES = ['US', 'GB']

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        self.last_fetch = 0
        self.cache = {}
        for img in Image.objects.raw("""SELECT * FROM core_image WHERE NOT EXISTS
                                        (SELECT 1 FROM core_imagelocation WHERE image_id = core_image.id)"""):
            preposition, location = self.geocode(img.latitude, img.longitude)
            ImageLocation.objects.create(image=img, preposition=preposition, location=location)
            print img.code, img.latitude, img.longitude, preposition, location

    def geocode(self, latitude, longitude):
        data = self.find_nearby(latitude, longitude)
        adm1 = None
        if data.find('ocean') is not None:
            # We're over an ocean
            return "over the", data.find('ocean/name').text
        elif data.find('country') is not None:
            # No populated places nearby, but we have a country
            return "over", data.find('countryName').text
        elif data.find('address') is not None:
            # We have an "address"-style response. Whatever that is.
            name_parts = [data.find('address/placename').text]
            if data.find('address/adminName1') is not None:
                adm1 = data.find('address/adminName1').text
            country_code = data.find('address/countryCode').text
        elif len(data.findall('geoname')) > 0:
            place_node = data.find('geoname[last()]')
            name_parts = [place_node.find('name').text]
            if data.find('geoname[fcode="ADM1"]') is not None:
                adm1 = data.find('geoname[fcode="ADM1"]/name').text
            country_code = place_node.find('countryCode').text

        if country_code in ADM1_COUNTRIES and adm1 is not None:
            # We've decided to show the ADM1 (state) here.
            name_parts.append(adm1)

        name_parts.append(countries.get(alpha2=country_code).name)
        return "near", ", ".join(part for part in name_parts if part is not None)

    def find_nearby(self, latitude, longitude, radius=10):
        params = {'lat': latitude, 'lng': longitude,
                  'cities': 'cities15000', 'username': USERNAME}
        if radius is not None:
            params['range'] = radius

        cache_key = (latitude, longitude, radius)
        if cache_key in self.cache:
            result = self.cache[cache_key]
        else:
            result = self.fetch('%s/extendedFindNearby' % ENDPOINT, params=params)

        data = lxml.etree.fromstring(result)
        error = data.find('status')
        if error is not None:
            value = error.get('value')
            if value == '24' and radius > 1:
                # In some areas of the world, geonames restricts our radius, so try without.
                return self.find_nearby(latitude, longitude, radius=None)
            elif value == '19':
                print "Hourly rate limit exceeded. Sleeping for 5mins."
                sleep(300)
                return self.find_nearby(latitude, longitude, radius=radius)
            elif value == '18':
                raise Exception("Daily rate limit exceeded!")
            elif value == '12':
                print "Unknown Geonames error, sleeping for 10 seconds"
                sleep(10)
                return self.find_nearby(latitude, longitude, radius=radius)
            else:
                raise Exception("Unhandled Geonames error: %s" % value)
        self.cache[cache_key] = result
        return data

    def fetch(self, url, **kwargs):
        elapsed = time() - self.last_fetch
        if elapsed < RATE:
            sleep(RATE - elapsed)
        self.last_fetch = time()

        result = requests.get(url, **kwargs)
        return result.content
