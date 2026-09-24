install:
	pip install -r requirements.txt
	playwright install --with-deps chromium

test:
	pytest -n 4

smoke:
	pytest -m smoke -n 4

headed:
	pytest --headed -n 0

report:
	allure serve allure-results

clean:
	rm -rf allure-results allure-report artifacts .pytest_cache