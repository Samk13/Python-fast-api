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

start the Server:

```zsh
uvicorn app.main:app --reload
```

to remove the **pycache** folder:
[link](http://www.randallkent.com/2010/04/30/gitignore-not-working/)
[github](https://github.com/martinohanlon/flightlight/issues/1)

```zsh
git rm -r --cached . && git add . && git commit -m "fixing .gitignore"
```
