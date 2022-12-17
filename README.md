```
$ python -m venv .venv

# Windows
$ Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
$ .venv\Scripts\Activate.ps1

# macOS
$ source .venv/bin/activate

(.venv) $ pip install -r requirements.txt
(.venv) $ python manage.py migrate
(.venv) $ python manage.py createsuperuser
(.venv) $ python manage.py loaddata item_status
(.venv) $ cp .env.example .env
Add GAPI and PROJECT_CX keys to .env file
(.venv) $ python manage.py runserver
# Load the site at http://127.0.0.1:8000
```