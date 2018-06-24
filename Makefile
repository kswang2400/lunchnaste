clean:
	find . -name \*.cache -delete
	find . -name \*.coverage -delete
	find . -name \*.pyc -delete
	find . -name \__pycache__ -delete
	find . -name \.pytest_cache -delete