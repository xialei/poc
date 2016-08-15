python
======

> 1. memsql: mysql replication to memsql
	
	https://github.com/memsql/ditto
	
	mysqldump
	
	$ mysqldump -h 127.0.0.1 -u root -B [database name] --no-data > schema.sql
	$ mysqldump -h 127.0.0.1 -u root -B [database name] --no-create-info > data.sql
	
	$ mysql -h 127.0.0.1 -u root -P 3307 < schema.sql
	$ mysql -h 127.0.0.1 -u root -P 3307 < data.sql

> 2. crawler

> 3. algorithm

> 4. mysql
	
	pip install cython
	pip install cymysql
	
> 5. gevent

	http://xlambda.com/gevent-tutorial/
	
> 6. gui

	autodriving (python, numpy, pandas, matplotlib, pyglet)	
	
> 7. machine learning

	pytesser，OCR in Python using the Tesseract engine from Google
	
	python-opencv : download opencv and cmake, make, makeinstall, cp cv.so to python directory
	
> 8. nlp

	pip install --no-index --upgrade scipy-0.18.0-cp27-cp27m-win_amd64.whl

	pip install --upgrade gensim
	
	conda install numpy
	