init:
	pip install pipenv
	pipenv install --dev
	pipenv install codecov


test:
	pipenv run isort --recursive --check-only --diff movie_plist
	pipenv run flake8 .
	pipenv run cov_all

report:
	pipenv run codecov