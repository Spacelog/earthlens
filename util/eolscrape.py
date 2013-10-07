from __future__ import division, absolute_import, print_function, unicode_literals
from os import path
from time import sleep
import sys
import requests
from lxml.html.soupparser import fromstring
from lxml.etree import tostring

OUTPUT = sys.argv[2]
PIXEL_THRESHOLD = 500000 # the smallest image we care about (pixels)
SIZE_THRESHOLD = 10000000 # largest file we want (MB)

def metadata_url(mission, roll, frame):
    return "http://eol.jsc.nasa.gov/scripts/sseop/photo.pl?mission=%s&roll=%s&frame=%s" % \
                    (mission.strip(), roll.strip(), frame.strip())

def fetch_metadata(mrf):
    url = metadata_url(*mrf)
    resp = requests.get(url)
    if resp.status_code != 200:
        raise Exception("Failure fetching URL %s: %s" % (url, resp.status_code))
    return resp.text

def extract_images(metadata):
    root = fromstring(metadata)
    imgtable = root.find('.//*[@id="MainTable"]//table')

    images = []
    for image in imgtable.findall('.//tr')[1:]:
        cells = image.findall('.//td')
        images.append({'url': cells[0].find('./a').get('href'),
                       'file': cells[1].text.strip(),
                       'size': int(cells[2].text),
                       'width': int(cells[3].text),
                       'height': int(cells[4].text)
                      })

    return images

def save_image(images):
    for image in images:
        if image['width'] * image['height'] < PIXEL_THRESHOLD:
            continue
        if image['size'] > SIZE_THRESHOLD:
            continue
        url = "http://eol.jsc.nasa.gov" + image['url']
        resp = requests.get(url)
        if resp.status_code == 200:
            suffix = url.split('.')[-1]
            with open(path.join(OUTPUT, image['file']), 'w') as f:
                f.write(resp.content)
            return True
        elif resp.status_code == 404:
            continue
        else:
            raise Exception("Failure fetching image %s: %s" % (url, resp.status_code))
    return False

with open(sys.argv[1], 'r') as f:
    data = f.readlines()

for line in data:
    mrf = tuple(field.strip() for field in line.strip("\t \n").split("\t")[0:3])
    metadata_file = path.join(OUTPUT, '%s-%s-%s.html' % mrf)
    if path.exists(metadata_file):
        continue

    print("Fetching %s-%s-%s" % (mrf[0], mrf[1], mrf[2]))
    metadata = fetch_metadata(mrf)

    possible_images = extract_images(metadata)
    if not save_image(possible_images):
        print("Skipping due to no suitable image (available images: %s)" % possible_images)
        continue

    with open(metadata_file, 'wb') as f:
        f.write(metadata)
    sleep(1)
