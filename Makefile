server:
	./env/bin/python ./manage.py runserver 0.0.0.0:8000

upgrade: env
	./env/bin/pip install -U -r ./requirements.txt

env:
	virtualenv --system-site-packages ./env
