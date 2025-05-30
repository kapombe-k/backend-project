#Import fastapi package
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from models import get_db, Patient, Visit, Doctor, Appointment, Prescription

#initialize it

app = FastAPI()

#this allows network requests from all servers
app.add_middleware(CORSMiddleware, allow_origins=['*'])

#define the routes
@app.get('/')
def index():
    return{'message':'Up and running'}

@app.get('/patients')
def all_patients(session = Depends(get_db)):
    #sqlalchemy retrieves all patients from the table
    all_patients = session.query(Patient).all()
    return all_patients

# http://localhost:9000/products -> GETs a single patient
@app.get('/patients/{id}')
def get_patients(session = Depends(get_db)):
    patient_id = session.query(Patient)
    print("Patient id", id)
    return patient_id

# http://localhost:9000/products -> POST
@app.post('/patients')
def add_patients():
    return {'message':'Patient added successfully'}

@app.patch('/patients/{id}')
def update_patient(id:int):
    print(f'Patient {id} has been updated')
    return {'message':'Patient added successfully'}

@app.delete('/patients/{id}')
def delete_patient(id:int):
    print(f'Patient {id} has been deleted')
    return {'message':'Patient deleted successfully'}

    
