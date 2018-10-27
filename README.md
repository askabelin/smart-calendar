# Smart Calendar

### Development on MacOS

Install:

    brew install python pipenv git sqlite
    git clone git@github.com:askabelin/smart-calendar.git
    cd smart-calendar/smartcalendar
    pipenv install --dev
    
Create database structure:

    pipenv run python manage.py migrate
    
Run tests:   
 
    pipenv run python manage.py test
    
Create admin user:

    pipenv run python manage.py createsuperuser

Start development server:
 
    pipenv run python manage.py runserver

Admin console is available on [http://localhost:8000/admin](http://localhost:8000/admin).


### Manual testing

* Login into the admin console.
* Create a users with username `interviewer` and password `123`. Add it to `interviewers` group.
* Create a users with username `candidate` and password `123`. Add it to `candidates` group.
* Create an available slot for the interviewer:
```
curl http://interviewer:123@localhost:8000/available-slots \
-X POST -H "Content-Type: application/json" \
--data '{"start":"2018-11-20T9:30","end":"2018-11-20T14:30"}'
```
* Create an available slot for the candidate:
```
curl http://candidate:123@localhost:8000/available-slots \
-X POST -H "Content-Type: application/json" \
--data '{"start":"2018-11-20T11:30","end":"2018-11-20T16:30"}'
``` 
* Request available interview slots for the candidate (id 3) with the interviewer (id 2):
```
curl http://localhost:8000/interview-slots/3?interviewers=2
```

Expected output:
```
[{"start":"2018-11-20T12:00:00","end":"2018-11-20T13:00:00"},
{"start":"2018-11-20T13:00:00","end":"2018-11-20T14:00:00"}]
```

