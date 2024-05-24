#!/usr/bin/env bash

# exit on error
set -o errexit

# pipefail ensures that a pipeline will produce a failure return code
# if any command errors.
set -o pipefail

# print commands before executing them
set -o xtrace

# install dependencies
if [[ ! -x "$(command -v curl)" ]]; then
  echo 'Error: curl is not installed.' >&2
  exit 1
fi

if ! curl -fsS https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -; then
  echo 'Error: Failed to add Docker GPG key.' >&2
  exit 1
fi

sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt-get update
sudo apt-get install -y docker-ce

# run as non-root user
if ! id -u django >/dev/null 2>&1; then
  sudo useradd -m -s /bin/bash django
fi

if ! groups django | grep -qw docker; then
  sudo usermod -aG docker django
fi

sudo chown django:django /var/run/docker.sock

su -c "pip install --upgrade pip" django
su -c "pip install -r requirements.txt" django

su -c "python manage.py collectstatic --no-input" django
su -c "python manage.py migrate" django
