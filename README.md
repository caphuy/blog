On windows
Prepare: Create db named "test" in local mysql
Step 1: Create venv
    $ python -m venv env
Step 2: Active virtural env
    $ env\bin\activate
Step 3: Install requirements
    $ pip install -r requirements.txt
Step 4: Init and migrate db
    $ python migrate.py db init
    $ python migrate.py db migrate
    $ python migrate.py db upgrade
Step 5: Run project
    $ python run.py

Import Got it.postman_collection.json to postman to see demo requests api
Link embedded to login: http://localhost:5000/user/authorize/facebook
                        http://localhost:5000/user/authorize/google