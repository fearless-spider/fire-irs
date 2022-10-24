PROJECT_NAME = fire-irs
SHELL := /bin/sh
help:
	@echo "Please use 'make <target>' where <target> is one of"
	@echo "  all                      to setup the whole development environment for the project"
	@echo "  env                      to create the virtualenv for the project"
	@echo "  setup_tests              install tests requirements to the virtualenv"
	@echo "  docs                     generate docs"
	@echo "  test                     run tests"


HERE = $(shell pwd)
VENV = $(HERE)/venv
BIN = $(VENV)/bin
PYTHON = $(BIN)/python3
VIRTUALENV = python3 -m venv
MAKE = make

.PHONY: clean env test docs

all: .PHONY

env:
	$(VIRTUALENV) $(VENV)

clean:
	rm -rf $(VENV)
	find . -name "*.pyc" -exec rm -rf {} \;

test_dependencies:
	$(BIN)/pip3 install tox

test: test_dependencies
	$(BIN)/tox

docs_depedencies:
	$(BIN)/pip3 install -e ".[docs]"

docs: docs_depedencies
	cd docs && $(MAKE) html SPHINXBUILD=$(BIN)/sphinx-build

setup_tests:
	$(BIN)/pip3 install -e ".[tests]"
