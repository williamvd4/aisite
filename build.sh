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

# add Docker GPG key
if ! curl -fsS https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -; then
    echo "Error: Failed to add Docker GPG key."
    exit 1
fi

# add Docker repository
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"

# update package list
sudo apt-get update

# install Docker
sudo apt-get install -y docker-ce

# check if user 'django' exists
if ! id -u django > /dev/null 2>&1; then
    # create user 'django'
    sudo useradd -m -s /bin/bash django
fi

# add user 'django' to the 'docker' group
if ! groups django | grep -qw docker; then
    sudo usermod -aG docker django
fi

# give 'django' user ownership of the Docker socket
sudo chown django:django /var/run/docker.sock

# upgrade pip and install requirements
sudo -u django -H pip install --upgrade pip || { echo "Error: Failed to upgrade pip."; exit 1; }
sudo -u django -H pip install -r requirements.txt || { echo "Error: Failed to install requirements."; exit 1; }

# collect static files and apply migrations
sudo -u django -H python manage.py collectstatic --no-input || { echo "Error: Failed to collect static files."; exit 1; }
sudo -u django -H python manage.py migrate || { echo "Error: Failed to apply migrations."; exit 1; }
