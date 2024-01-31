# django-rest-framework-demo

## Pre-requisites:

1. Docker 
2. VSCode
3. VSCode Dev Containers extension
4. VSCode Docker extension

## How the aplication was generated 

1. Create a folder for your project and navigate into it
2. Create a virtual environment and install cookiecutter  using the command 

``` pip install cookiecutter ```

Run the command:

```cookiecutter https://github.com/erwazzzzzzz2/simple-django-cookie-cutter-template.git```

The stub project is generated

- .devcontainer
- baseproject
    - __init__.py
    - asgi.py
    - settings.py
    - urls.py
    - wsgi.py
- core
    - managemant
        - commands
            - __init__.py
            - rename_proect.py
            - run_app.py
            - wait_for_db.py
    - migrations
    - tests
    - __init__.py
    - admin
    - apps.py
    - models.py

- .dockerignore
- .flake8
- docker-cmpose.debug.yml
- docker-compose.yml
- Dockerfile
- manage.py
- README.md
- requirements.txt


To the above  were added 

1. GitHub actions 
2. order app
