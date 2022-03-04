Run these commands if you get database migrations related problems

python manage.py makemigrations api
python manage.py migrate


If you get ModuleNotFound error, run this. 

pip install -r requirements.txt

If you install any other library make sure you add it to requirements.txt

### How to add new library to requirement.txt?

Delete the existing requirements.txt
And run the command:

pip freeze > requirement.txt

