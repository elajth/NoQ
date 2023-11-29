# noQ
1558 personer sover ute i natt i Stockholm, dvs akut hemlösa. 
Våra tankar i team noQ går till Er och vi kämpar för att ni ska slippa stå i kö varje dag för en eventuell sovplats.

## .env file for settings
DATABASE_URL=sqlite:///noq.sqlite

## create database tables
```
python 'generate sqlmodel.py'
python generate.py (after running the "uvicorn main:app" once)
```
## To run
```
uvicorn main:app
```