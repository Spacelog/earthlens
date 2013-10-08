server:
	./env/bin/python ./manage.py runserver

upgrade: env
	./env/bin/pip install -U -r ./requirements.txt

env:
	virtualenv ./env
