#!/bin/bash

set -e

coverage erase
# coverage run --source=. -m examples.simplest.bot
coverage run -a --source=. -m deepdialog.train ./examples/simplest/ /tmp/m
coverage run -a --source=. -m deepdialog.serve /tmp/m < ./examples/simplest/sample.txt
coverage report -m