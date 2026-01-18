SHELL := /bin/bash

prepare-venvironment:
	@echo "Installing the project's dependencies..."
	(rm -rf venv \
	&& python3 -m venv venv \
	&& source venv/bin/activate \
	&& python3 -m pip install -r requirements.txt)
	@echo "The Project's environment is ready!!"