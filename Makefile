init:
	pip install pipenv
	pipenv install --dev
	pipenv install codecov
	pipenv install mypy


test:
	pipenv run isort --recursive --check-only --diff movie_plist
	pipenv run flake8 .
	pipenv run mypy movie_plist/data/check_dir.py
	pipenv run mypy movie_plist/data/create_dict.py
	pipenv run mypy movie_plist/data/fetch_data.py
	pipenv run cov_all

report:
	pipenv run codecov

clean:
	rm -fr .pytest_cache
	rm -fr .coverage
	rm -fr .tox
	rm -fr movie_plist.egg-info
	rm -fr .mypy_cache
	find ./ -name '__pycache__' -type d | xargs rm -fr
