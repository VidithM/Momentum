.PHONY: requirements
requirements:
	pip-compile --resolver=backtracking pyproject.toml

.PHONY: run
run:
	python -m app --reload --port=8020