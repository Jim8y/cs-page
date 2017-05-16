PWD=$(shell pwd)

all: deploy-s3 deploy-cornell

css:
	pwd
	pushd $(PWD)/semantic && gulp build && popd

website:
	test -d env && source env/bin/activate && python main.py && deactivate

deploy-cornell: website
	rsync -avh --delete output/ fanz@lion.cs.cornell.edu:/home/WIN/fanz/MyWeb/

deploy-s3: website
	aws s3 sync output/ s3://www.fanzhang.me 
