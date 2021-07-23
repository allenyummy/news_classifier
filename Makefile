init:
	pip install -r requirements.txt

test:
	nosetests -v tests

prepare_dev_env:
	pip install poetry && poetry install && pre-commit install

prepare_production_env:
	pip install poetry && poetry install --no-dev

show:
	poetry show

show_dependency:
	poetry show --tree && \  ## colorful terminal
	poetry show --tree > dependencies.txt
	# poetry show --tree 2>&1 | tee dependencies.txt

freeze_package:
	poetry export --without-hashes -f requirements.txt --output requirements.txt

test-pytest:
	pytest tests/ --log-cli-level=warning --cov=./ --cov-report term-missing
