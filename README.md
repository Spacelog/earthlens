Earth Lens
==========

Earth Lens is a project to take the images published by NASA
of Earth from space - all taken by astronauts on orbital missions -
and allow them to be easily viewed and curated for quality and
type of content.

The site is a Django application that ingests the original
HTML pages the images are published on, and that expects the images
in a predefined location (by default, static/missions/SL2/large/SL2-1-232.jpg,
where SL2 is the mission code, and large is the image size).

There are three sizes of image: original, the original in JPEG format;
large, a scaled image with a width of 1800px or less; and square,
a cropped square image of 750x750px.


License
-------

The codebase is released under the [CC-0](http://creativecommons.org/publicdomain/zero/1.0/) license.

Note that the data obtained using the geocoding API is under a different license, [CC-0](http://creativecommons.org/publicdomain/zero/1.0/).


Running the code
----------------

The site is a standard Django application, so you're recommended to
read up on how they work if you're not familiar, but as a quick guide:

    virtualenv ./env/
    env/bin/pip install -r requirements.txt
    env/bin/python manage.py runserver
