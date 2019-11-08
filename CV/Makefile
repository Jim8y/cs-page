DATE=`date '+%F'`
CV_NAME="cv-fanzhang-${DATE}"

all: update
	@echo "copied :-)"

build:
	latexmk -pdf main.tex -jobname=${CV_NAME}

update: clean build
	cp ${CV_NAME}.pdf ../files/cv_fanzhang.pdf
	cp ${CV_NAME}.pdf ~/Dropbox/Job\ market

clean:
	rm -rf *.pdf

