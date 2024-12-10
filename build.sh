#!/usr/bin/env bash

# exit on error
set -o errexit

# pipefail ensures that a pipeline will produce a failure return code
# if any command errors.
set -o pipefail

# print commands before executing them
set -o xtrace

# check if curl is installed
if ! command -v curl > /dev/null 2>&1; then
    echo "Error: curl is not installed."
    exit 1
fi

# upgrade pip and install requirements
pip install --upgrade pip || { echo "Error: Failed to upgrade pip."; exit 1; }
pip install -r requirements.txt || { echo "Error: Failed to install requirements."; exit 1; }

# collect static files and apply migrations
python manage.py collectstatic --no-input || { echo "Error: Failed to collect static files."; exit 1; }
python manage.py migrate || { echo "Error: Failed to apply migrations."; exit 1; }
