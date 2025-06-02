#Import fastapi package
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from schemas import PatientsSchema, VisitsSchema, DoctorsSchema, AppointmentsSchema
from sqlalchemy.orm import Session 
from models import get_db, Patient, Visit, Doctor, Appointment

#initialize it

app = FastAPI()

#this allows network requests from all servers
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

#define the routes
@app.get('/')
def index():
    return{'message':'Up and running'}

@app.get('/patients')
def all_patients(session: Session = Depends(get_db)):
    #sqlalchemy retrieves all patients from the table
    all_patients = session.query(Patient).all()
    return all_patients

# http://localhost:8000/patients -> GETs a single patient
@app.get('/patients/{id}')
def get_patient(session = Depends(get_db)):
    patient_id = session.query(Patient)
    print("Patient id", id)
    return patient_id

# http://localhost:8000/patients -> POST
@app.post('/patients')
def add_patients(patient:PatientsSchema, session= Depends(get_db)):
    # create an instance of the product model with the values
    #instead of:
    #new_patient = Patient(name=patient.name, age=patient.age, phone_number=patient.phone_number, address=patient.address, account_types=patient.account_type)
    new_patient = Patient(**patient.model_dump())
    # add the product to the transaction
    session.add(new_patient)
    # comit the transaction
    session.commit()
    return {'message':'Patient posted successfully'}

@app.patch('/patients/{id}')
def update_patient(id:int, patient:PatientsSchema, session = Depends(get_db)):
    print(f'Patient {id} has been updated')
    return {'message':'Patient patched successfully'}

@app.delete('/patients/{id}')
def delete_patient(id:int):
    print(f'Patient {id} has been deleted')
    return {'message':'Patient deleted successfully'}

@app.post('/visits')
def add_visit(visit: VisitsSchema, session = Depends(get_db)):
    #create an instance model of the visits
    new_visit = Visit(**visit.model_dump())
    #add the visit
    session.add(new_visit)
    #commit visit to the db
    session.commit()
    return {'message':'Visit added successfully'}

@app.patch('/visits/{id}')
def update_visit(visit: VisitsSchema, session = Depends(get_db)):
    update_visit = Visit(**visit.model_dump())
    #patch the visit
    session.add(update_visit)
    #commit the visit to the db
    session.commit()
    return {'message':'Visit fixed'}

@app.delete('/visits/{id}')
def delete_visit(visit: VisitsSchema, session = Depends(get_db)):
    delete_visit = Visit(**visit.model_dump())
    #delete the visit
    session.delete(delete_visit)
    #commit the delete
    session.commit()
    return {'message':'visit deleted successfully'}

@app.post('/appointments')
def add_appointment(visit:AppointmentsSchema, session = Depends(get_db)):
    #create an instance model of the visits
    new_appointment = Appointment(**appointment.model_dump())
    #add the visit
    session.add(new_appointment)
    #commit visit to the db
    session.commit()
    return {'message':'appointment added successfully'}

@app.patch('/appointments/{id}')
def update_appointment(visit: AppointmentsSchema, session = Depends(get_db)):
    update_appointment = Appointment(**appointment.model_dump())
    #patch the visit
    session.add(update_appointment)
    #commit the visit to the db
    session.commit()
    return {'message':'appointment fixed'}

@app.delete('/appointments/{id}')
def delete_appointment(appointment: AppointmentsSchema, session = Depends(get_db)):
    delete_appointment = Appointment(**appointment.model_dump())
    #delete the visit
    session.delete(delete_appointment)
    #commit the delete
    session.commit()
    return {'message':'appointment deleted successfully'}

@app.post('/doctors')
def add_doctors(doctors: DoctorsSchema, session = Depends(get_db)):
    #create an instance model of the visits
    new_doctors = Doctor(**doctors.model_dump())
    #add the visit
    session.add(new_doctors)
    #commit visit to the db
    session.commit()
    return {'message':'doctors added successfully'}

@app.patch('/doctors/{id}')
def update_doctors(doctors: DoctorsSchema, session = Depends(get_db)):
    update_doctors = Doctor(**doctors.model_dump())
    #patch the visit
    session.add(update_doctors)
    #commit the visit to the db
    session.commit()
    return {'message':'doctors fixed'}

@app.delete('/doctors/{id}')
def delete_doctors(doctors: DoctorsSchema, session = Depends(get_db)):
    delete_doctors = Doctor(**doctors.model_dump())
    #delete the visit
    session.delete(delete_doctors)
    #commit the delete
    session.commit()
    return {'message':'doctor deleted successfully'}


