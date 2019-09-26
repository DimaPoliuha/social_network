# social network

## Setup
```sh
# Install dependencies
pipenv install --dev

# Setup pre-commit and pre-push hooks
pipenv run pre-commit install -t pre-commit

pipenv shell
```

#### Create `.env` file in `social_network` folder
```.env
DJANGO_SECRET_KEY="specify"
DB_NAME="specify"
DB_USER="specify"
DB_PASS="specify"
DB_HOST="specify"
DB_PORT="specify"
EMAIL_HOST_USER="specify"
EMAIL_HOST_PASSWORD="specify"
EMAIL_HOST="specify"
EMAIL_PORT="specify"
```

## Run
```sh
python manage.py runserver
```
