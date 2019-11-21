DATE=`date '+%F'`
CV_NAME="cv-fanzhang-${DATE}"
CV_WITH_REF_NAME="cv-ref-fanzhang-${DATE}"

all: update
	@echo "copied :-)"

build:
	latexmk -pdf main.tex -jobname=${CV_NAME}
	latexmk -c main.tex -jobname=${CV_NAME}
	latexmk -pdf cv_with_ref.tex -jobname=${CV_WITH_REF_NAME}
	latexmk -c cv_with_ref.tex -jobname=${CV_WITH_REF_NAME}

update: clean build
	cp ${CV_NAME}.pdf ../files/cv_fanzhang.pdf
	cp ${CV_NAME}.pdf ~/Dropbox/Job\ market
	cp ${CV_WITH_REF_NAME}.pdf ~/Dropbox/Job\ market

clean:
	rm -rf *.pdf

