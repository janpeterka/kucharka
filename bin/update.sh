#!/bin/bash

cd /home/kucharka/kucharka

# ensure to get origin's data and discard any local change
git fetch
git reset origin/master --hard
git pull

# install python packages
pipenv install

# install javacript packages
cd /home/kucharka/kucharka/app/static
npm ci
npm run build

# upgrade database
pipenv run flask db upgrade
