DATE=`date '+%Y-%m-%d'`
CV_NAME="cv-fanzhang-${DATE}.pdf"


all: update
	@echo "copied :-)"

build:
	latexmk -pdf main.tex
	mv main.pdf ${CV_NAME}

update: clean build
	cp ${CV_NAME} ../files/cv_fanzhang.pdf

clean:
	rm -rf *.pdf

