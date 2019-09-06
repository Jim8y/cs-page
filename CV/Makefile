clean:
	rm -rf *.pdf

build:
	latexmk -pdf main.tex

update: clean build
	cp main.pdf ../files/cv_fanzhang.pdf
