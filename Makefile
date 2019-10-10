test:
	pytest .

cov:
	pytest . --cov=queryfilter --cov-report=html
