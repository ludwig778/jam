run:
	fbs run

sh:
	bash

py:
	ipython3 --no-confirm-exit --colors=Linux

isort:
	python3 -m isort

test:
	pytest -vs

cov:
	pytest --cov

cov_html:
	pytest --cov --cov-report html

lint:
	python3 -m flake8

piprot:
	piprot

sure: isort coverage lint piprot

clean:
	find . -name "*.pyc" -o -name "__pycache__" | tac | xargs rm -rf
