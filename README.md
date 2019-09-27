# social network

## Prerequisites
Make sure you have installed all of the following prerequisites on your development machine:
- Python3.7
- [Pipenv](https://pipenv.readthedocs.io/en/latest/)
- [PostgreSQL](https://www.postgresql.org/)

## Setup
```shell script
# Install dependencies
pipenv install
# or for development
# pipenv install --dev

# Only for development
# pipenv run pre-commit install -t pre-commit

pipenv shell
```

You need to create db and create `.env` file in `social_network` folder from this template:

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
CLEARBIT_API="specify"
EMAILHUNTER_API="specify"
```
You need to make migrations and create superuser/admin for server:
```shell script
python manage.py makemigrations

python manage.py migrate

python manage.py createsuperuser
```

## Run
```shell script
python manage.py runserver
```

## Usage

Type `http://127.0.0.1:8000/` in your browser.

Also, this application has following API endpoints:

- `/api/v1/posts/` - view all posts
- `/api/v1/users/` - view all users
- `/api/v1/likes/` - view all likes
- `/api/v1/token/` - login
- `/api/v1/token/refresh/` - refresh auth token
- `/api/v1/signup/` - register
- `/api/v1/posts/create/` - create post
- `/api/v1/posts/like/` - like/dislike


## Examples
```shell script
http post http://127.0.0.1:8000/api/v1/token/ username="user" password="hfugrwehg324"

http post http://127.0.0.1:8000/api/v1/posts/create author="12314" post_text="post" post_title="test" "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTY5NTgyOTc5LCJqdGkiOiJjN2IyZTNiNjUwYzI0Y2ZmOWY1ODQwMzI0NThjNGI4MSIsInVzZXJfaWQiOjQ3fQ.3IO-T1XrcBThe5hYjU9ALkTrhtigFG1Bc1LHJUHysb8"

http post http://127.0.0.1:8000/api/v1/posts/like user_id=47 post_id=46 "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTY5NTgzODkwLCJqdGkiOiI2MDAwN2E4YjZlYmE0NjNlOWI5OTQ3OThmNDM0NDlmNCIsInVzZXJfaWQiOjQ3fQ.YJj5t-QLH9qDda-Ou5qb_nEgo57YRjVSoHLokHgXnw8"
```
