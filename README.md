# Portfolio

A Django portfolio site with profile, qualification, resume, and marksheet pages.

## Run locally

Install the dependencies with Pipenv, then run the Django commands from the `first` directory:

```powershell
pipenv install
cd first
pipenv run python manage.py migrate
pipenv run python manage.py runserver
```

Set the `DJANGO_SECRET_KEY` environment variable to a unique secret before deploying. The fallback key in settings is for local development only.

The local SQLite database and private uploaded files are intentionally excluded from GitHub. Create a staff account with `pipenv run python manage.py createsuperuser` and add portfolio details through `/admin/`.
