all: update
	@echo "copied :-)"

build:
	latexmk -pdf main.tex

update: clean build
	cp main.pdf ../files/cv_fanzhang.pdf

clean:
	rm -rf *.pdf

