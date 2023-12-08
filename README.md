# noQ

Sovplatser för hemlösa

## .env file for settings

DATABASE_URL=sqlite:///noq.sqlite OR other database url

## create database tables

``` python
python 'generate sqlmodel.py'
python generate.py (after running the "uvicorn main:app" once)
```

## To run

```bash
uvicorn main:app
```
