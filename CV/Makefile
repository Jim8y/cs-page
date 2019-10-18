clean:
	rm -rf *.pdf

build:
	latexmk -pdf -xelatex main.tex

update: clean build
	cp main.pdf ../files/cv_fanzhang.pdf
