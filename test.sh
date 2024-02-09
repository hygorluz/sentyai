#!/bin/bash
#####
# RUN UNIT TESTS AND CODE GUIDE CHECKS
#####

# Exit if any command fails
set -e

# Auto format our code
echo "Formatting code..."
python -m yapf --exclude 'venv/**/*' --in-place -r .

# Execute the code guidelines checks
echo "Running the style guide checker..."
python -m flake8 . || (echo "Problems with the code style, please review the logs." && exit 1)

# Linter
python -m pylint --fail-under 9.25 --jobs 0  --recursive y .  || (echo "Too many issues detected by pylint, please solve the issues above." && exit 1)

# Run the unit tests
echo "Running unit tests..."
python -m coverage run -m unittest

# Prepare the code coverage reports
echo "Creating the code coverage reports..."
python -m coverage report -m --fail-under 65 || (echo "The unit test coverage is too small, please increase the code coverage." && exit 1)
python -m coverage xml

