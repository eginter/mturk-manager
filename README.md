# MTurk Manager
This repository is intended to completely replace the requester site web page of Mechanical Turk.

The user is able to manage projects, upload batches, create different templates for better reviewing the results and many more.

The instructions can be found in the [Wiki](https://github.com/webis-de/mturk-manager/wiki) of this repository.  

The whole tool is built on top of the [Django-Framework](https://www.djangoproject.com/).  

## Requirements
* Python 3.6+

## Frontend

### Installation / Update

**Note:** If you want to use a virtual environment like `virtualenv` switch to the virtual environment before executing the following step!

1. Execute `./setup.sh` to pull changes from the repository and install missing dependencies.

### Run Server
1. Execute `cd mturk`
2. Execute `python3 manage.py runserver 8000` to start the server _([more](https://docs.djangoproject.com/en/2.2/ref/django-admin/#django-admin-runserver) on how to start a django server)_
3. Visit [localhost:8000](http://localhost:8000)

**Note** You can safely ignore the following message in the terminal: `You have XXX unapplied migration(s)`.  
You can execute `python3 manage.py migrate` if the message bothers you.

## Backend

### Installation / Update
1. Execute `./setup_db.sh` to pull changes from the repository and install missing dependencies.
2. Execute `cd mturk`
3. Execute `python3 manage.py migrate`

### Run Server
1. Run `cd mturk_db`
2. Run `python3 manage.py runserver 8001` to start the server _([more](https://docs.djangoproject.com/en/2.2/ref/django-admin/#django-admin-runserver) on how to start a django server)_
3. Visit [localhost:8001](http://localhost:8001)

## Supported Features
* Create and manage mechanical turk projects
* Define **multiple** worker templates per project
* Customize the layout of the worker results
* Extensive approve/reject facility

## Contributors
* Kristof Komlossy
* Martin Potthast
* Matthias Hagen
* Florian Kneist

## Contact
Did you find a bug or do you have questions/requests?  
Write me a mail: mturk@kritten.org
