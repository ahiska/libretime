all: lint test

include ../tools/python.mk

PIP_INSTALL = --editable .[dev]
PYLINT_ARG = libretime_shared tests
MYPY_ARG = libretime_shared
PYTEST_ARG = --cov=libretime_shared tests

format: .format
lint: .pylint .mypy
test: .pytest
clean: .clean
