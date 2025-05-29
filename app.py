#Import fastapi package
from fastapi import FastAPI

#initialize it

app = FastAPI()

#define the routes
@app.get('/')
def index():
    return{'message':'Up and running'}

@app.get('/patients')
def patients():
    return []

@app.post('/patients')
def add_patients():
    return {'message':'Patient added successfully'}
    
