# Django CRM

Customer Relationship Management system written in Python


***To generate ER Diagrams***

` $env:FONTCONFIG_PATH = "C:\git\django_crm\fontconfig\"`

Then:

`python manage.py graph_models -a -o project_erd.png`

`python manage.py graph_models --pygraphviz -a -g -o ../devnotes/my_project_visualized.png`

Seems to overlap on Windows11

Default admin and password

**Collect static files**

`python manage.py collectstatic`

** Start the server **

`python manage.py runserver`

Notes:

using [grappelli](https://django-grappelli.readthedocs.io/en/latest/quickstart.html#installation) theme