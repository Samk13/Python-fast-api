
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat&labelColor=ef8336)](https://github.com/psf/black)
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>

# Fast API for Python

## setup:

make sure the venv is activated
run:

```bash
venv/Scripts/activate.bat

mac:
    source venv/Script/activate
```

to deactivate the venv:
deactivate

---

If you get errors with pip not found:
solution:

```bash
python -m ensurepip
```



to remove the **pycache** folder:
[link](http://www.randallkent.com/2010/04/30/gitignore-not-working/)
[github](https://github.com/martinohanlon/flightlight/issues/1)

```zsh
git rm -r --cached . && git add . && git commit -m "fixing .gitignore"
```

# Postman:
setup environment variable:

next to header and body, choose "Tests" paste the following:
`pm.environment.set("JWT", pm.response.json().access_token);`
this will set the environment variable JWT to the value of the access_token
you can set the variable in Environment left tab in Postman
- you can also set URL variable and replace your URL with `{{url}}`

## Setup Alembic:
[Setup Alembic](https://youtu.be/0sOvCWFmrtA?t=38242)

## run migration on heroku postgres db:
If you are on windows machine:
You should not use gitbas to run the commends, instead use powershell or cmd as follows:
```bash
heroku run "alembic upgrade head"
```
> Make sure after installing Heroku cli to close your terminal and restart VS code.


## Access postgres db from ssh:
### [setup postgres config to be accessed with ssh](https://youtu.be/0sOvCWFmrtA?t=44246)

---
### [Auto reboot app on restart setup service](https://youtu.be/0sOvCWFmrtA?t=46455)
---
### [Auto reboot app on restart](https://youtu.be/0sOvCWFmrtA?t=47042)
---
### [Setup Nginx](https://youtu.be/0sOvCWFmrtA?t=47088)
---

### [Setup HTTPS](https://youtu.be/0sOvCWFmrtA?t=47445)
---
### [Setup SSL](https://youtu.be/0sOvCWFmrtA?t=47723)
---
### [Setup Firewall](https://youtu.be/0sOvCWFmrtA?t=48013)
---
### [Setup app using Docker](https://youtu.be/0sOvCWFmrtA?t=48380)
---
### [Setup Docker compose](https://youtu.be/0sOvCWFmrtA?t=49121)
---
### [Optimize Docker for production](https://youtu.be/0sOvCWFmrtA?t=50942)
---
### [Deal with authentication testing](https://youtu.be/0sOvCWFmrtA?t=59311)
---



flags:
pytest --disable-warnings -> disable warnings
pytest -v -> verbose
pytest -s -> show output
pytest -x -> exit on first failure
pytest -v -rP -> Captured stdout calls like print statements


[my Horuku](https://sam-arbid-fastapi.herokuapp.com/docs)



# Start the Server:
```zsh
uvicorn app.main:app --reload
```

# run tests:
```zsh
pytest -v -rP
```
