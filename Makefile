PWD=$(shell pwd)

all: deploy-s3 deploy-cornell

website:
	test -d env && source env/bin/activate && python main.py && deactivate

compress:
	chmod u+x compress.sh && ./compress.sh

deploy-cornell: website
	rsync -avh --delete output/ fanz@lion.cs.cornell.edu:/home/WIN/fanz/MyWeb/

deploy-s3: website compress
	aws s3 sync --delete output/ s3://www.fanzhang.me
