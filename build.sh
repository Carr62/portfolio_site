#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

# Copy media files to static so WhiteNoise can serve them
mkdir -p staticfiles/media
cp -r media/* staticfiles/media/ || true

python manage.py collectstatic --no-input
python manage.py migrate --no-input