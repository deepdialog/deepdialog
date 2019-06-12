#!/bin/bash

set -e
flake8 ./deepdialog/*.py
flake8 ./deepdialog/**/*.py
flake8 ./examples/*.py
flake8 ./examples/**/*.py
pydocstyle deepdialog
