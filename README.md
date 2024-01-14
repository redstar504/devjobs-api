# DevJobs API

The backend portion of the Frontend Mentor devjobs challenge.

## Notable commands:

This command transforms the JSON data provided by FM into our own model representation:

`python manage.py mapfixtures --model <companies|jobs>`

The mapfixtures command generates JSON that can then be imported into our own database using:

`python manage.py loaddata <companies|jobs>.json`