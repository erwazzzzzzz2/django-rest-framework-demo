# Django development environment using VSCode Remote Containers

## Pre-requisites:

1. Docker 
2. VSCode
3. VSCode Dev Containers extension
4. VSCode Docker extension

## How to run the application

Its assumed VSCode is the IDE

Make  a directory to containg you project and cd into it.
Create a virtual environment and install cookiecutter  using the command 

``` pip install cookiecutter ```

Run the command:

```cookiecutter https://github.com/erwazzzzzzz2/simple-django-cookie-cutter-template.git```

Choose values for the prompts or accept the defaults

A new project folder should be created and inside; this a DevContainer Django/Postgres project.
navigate into the project
Select the VSCode command pallete and select Dev Containers: Rebuild Container 
You containerized environment should run. You might to be asked to install the Docker Extension , this is a bug see the DevContainer repo README mentioned below.

Run the command below to start the application and check the database is created.

``` python manage.py run_app```

If you want to change the Django project name use the command:

``` python manage.py rename_project <current_name> <new_name> ```

See the repo https://github.com/erwazzzzzzz2/django-devcontainers  for details of the devcontainer set up, issues and so on.
   
   




