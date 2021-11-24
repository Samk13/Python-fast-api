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

# Start the Server:

```zsh
uvicorn app.main:app --reload
```