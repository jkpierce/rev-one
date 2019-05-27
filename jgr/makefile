          NAME1 = rev-one
       PRODUCT1 = $(NAME1).pdf
     TEXSOURCE1 = $(NAME1).tex
     BBL1 = $(NAME1).bbl

      BIBINPUTS = biblio.bib

     PDFFIGURES = $(BUILTPDFFIGURES) ${PNGFIGURES}
     PNGFIGURES = 
     GIFFIGURES = 
     SVGFIGURES = 

all: $(PRODUCT1)

$(NAME1).pdf: $(TEXSOURCE1) $(BBL1) $(PDFFIGURES)
$(NAME1).dvi: $(TEXSOURCE1) $(BBL1) $(EPSFIGURES)
$(NAME1).bbl: $(TEXSOURCE1) $(BIBINPUTS) $(PDFFIGURES)

clean:
	$(RM) ${BUILTPDFFIGURES} $(NAME1).aux $(NAME1).dvi \
	    $(NAME1).log $(NAME1).blg $(NAME1).bbl $(NAME1).out \
	    $(NAME1).toc $(NAME1).lof $(NAME1).lot $(NAME1).brf \
            *.aux

# configuration issues
.SUFFIXES: .tex .pdf .bbl

PDFLATEX=	pdflatex
BIBTEX=		bibtex
XELATEX=	xelatex 
LATEX=		latex
BIBLATEX=	$(PDFLATEX)
BIBTEX=		bibtex -min-crossref=1000
RM=		rm -f
MV=		mv
CP=		cp -p

.tex.pdf:
	$(PDFLATEX) $(LATEXFLAGS) $<
	@while egrep -q 'LaTeX Warning:.*Rerun|Rerun to get' $*.log; do \
		  printf '\n' ; printf '#%.0s' {1..80} ; printf '\n' ; \
	      echo $(PDFLATEX) $<; \
	      $(PDFLATEX) $(LATEXFLAGS) $< || exit $$?; \
	done
	$(MV) $*.pdf out.pdf

.tex.bbl: 
	$(BIBLATEX) $(LATEXFLAGS) $<
	$(BIBTEX) $*
	$(RM) $*.aux $*.dvi $*.pdf 

