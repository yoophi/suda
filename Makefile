all:

# pip install sphinx
# pip install sphinxcontrib-httpdomain
# docs/_build/html/

makedocs:
	sphinx-apidoc -F -o docs sample/ --separate
	make clean -C docs && make html -C docs

makecleandocs:
	/bin/rm -f docs/*.rst
	sphinx-apidoc -F -o docs sample/ --separate
	make clean -C docs && make html -C docs
