PWD=$(shell pwd)
SHELL:=/bin/bash

all: deploy-s3 deploy-cornell

website:
	test -d env && source env/bin/activate && python main.py && deactivate

compress:
	chmod u+x compress.sh && ./compress.sh

deploy-cornell: website
	rsync -avh --delete output/ fz84@cslinux.cs.cornell.edu:/people/fz84/

deploy-s3: website compress
	aws s3 sync --delete output/ s3://www.fanzhang.me
