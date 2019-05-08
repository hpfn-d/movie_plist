init:
	pip install pipenv
	pipenv install --dev
	pipenv install codecov
	pipenv install mypy


test:
	pipenv run isort --recursive --check-only --diff movie_plist
	pipenv run flake8 .
	pipenv run mypy  movie_plist/data/pyscan.py
	pipenv run mypy  movie_plist/data/fetch_data.py
	pipenv run cov_all

report:
	pipenv run codecov
