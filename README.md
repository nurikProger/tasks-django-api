# tasks-django-api
Drf Task manager API

How to use:
1) Run /todolist/manage.py and add "runserver" in the end to run the server
2) Copy the url address of the local server and paste it to your browser's searchbar
3) Add one of these to the url:
  api/tasks/
  api/tasks/?start_date=&end_date=
  api/tasks/:id/
  api/tasks/to-do/
  api/tasks/expired/
  api/tasks/in_progress/
  api/tasks/done/
4) Use "YY-mm-dd HH:MM:SS" format for datetime inputs. Note! The input must contain digits for every value shown (month, day, seconds..)
