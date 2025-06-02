#Import fastapi packages
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from schemas import PatientsSchema, VisitsSchema, DoctorsSchema, AppointmentsSchema, PrescriptionSchemea
from sqlalchemy.orm import Session 
from models import get_db, Patient, Visit, Doctor, Appointment, Prescription

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

#======here we define the patient endpoints ========
# http://localhost:8000/patients -> GETs a single patient
@app.get('/patients')
def get_all_patients(session: Session = Depends(get_db)):
    #to get ALL patients from the db
    patients = session.query(Patient).all()
    print("Patient id", id)
    return patients

@app.get('/pateints/{patient_id}', response_model=PatientsSchema)
def get_patient(patient_id: int, session: Session = Depends(get_db)):
    # get patient by id
    patient = session.query(Patient).filter(Patient.id == patient_id)
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_Not_Found,
            detail= f"Patient wit ID {patient_id} not found"
        )
    return patient
    

# http://localhost:8000/patients -> POST
@app.post('/patients', status_code=status.HTTP_201_Created)
def add_patients(patient:PatientsSchema, session: Session = Depends(get_db)):
    # create an instance of the product model with the values
    # check nfor error on existing patient:
    existing_patient= session.query(Patient).filter(Patient.phone_number == patient.phone_number).first()
    if existing_patient:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= "Phone number already registered to another patient!"
        )
    #new_patient = Patient(name=patient.name, age=patient.age, phone_number=patient.phone_number, address=patient.address, account_types=patient.account_type)
    new_patient = Patient(**patient.model_dump())
    # add the product to the transaction
    session.add(new_patient)
    # comit the transaction
    session.commit()
    # refresh
    session.refresh(new_patient)
    return {'message':'Patient {new_patient.id} posted successfully!'}

@app.patch('/patients/{patient_id}')
def update_patient(patient_id:int, patient_data:PatientsSchema, session: Session = Depends(get_db)):
    # update patients' info
    patient = session.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_400_NOT_FOUND,
            detail= f"Patient with ID {patient_id} not found!"
        )
    session.commit()
    session.refresh(patient)
    print(f'Patient {id} has been updated')
    return {'message':'Patient {patient.id} patched successfully'}

@app.delete('/patients/{patient_id}')
def delete_patient(patient_id:int, session: Session = Depends(get_db)):
    # deletes a patient from db
    patient = session.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_400_NOT_FOUND,
            detail= f"Patient with ID {patient_id} not found!"
        )
    session.delete(patient)
    session.commit() 
    # final return
    return {'message':'Patient {patient_id} deleted successfully'}

# =====visit endpoints======
@app.get('/visits')
def get_all_visits(session: Session = Depends(get_db)):
    # get all visits from the db
    visit = session.query(Visit).all()
    return visit

@app.post('/visits', status_code=status.HTTP_201_CREATED)
def add_visit(visit: VisitsSchema, session: Session = Depends(get_db)):
    #Add a new visit to the database
    # Check if patient exists
    patient = session.query(Patient).filter(Patient.id == visit.patient_id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Patient with id {visit.patient_id} not found"
        )
    
    # Check if doctor exists
    doctor = session.query(Doctor).filter(Doctor.id == visit.doctor_id).first()
    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Doctor with id {visit.doctor_id} not found"
        )
    
    new_visit = Visit(**visit.model_dump())
    
    session.add(new_visit)
    session.commit()
    session.refresh(new_visit)
    return {
        "message": "Visit created successfully",
        "visit_id": new_visit.id
    }

@app.patch('/visits/{visit_id}')
def update_visit(visit_id: int, visit_data: VisitsSchema, session: Session = Depends(get_db)):
    #get a visit by id
    visit = session.query(Visit).filter(Visit.id == visit_id).first()
    if not visit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Visit with id {visit_id} not found"
        )
    return visit
    
    #add the visit
    #commit visit to the db
    session.commit()
    session.refresh(visit)
    return {'message':'Visit {visit.id} added successfully'}

@app.delete('/visits/{visit_id}')
def delete_visit(visit_id:int, session: Session = Depends(get_db)):
    #delete the visit from the db
    visit = session.query(Visit).filter(Visit.id == visit_id).first()
    session.delete(visit)
    #commit the delete
    session.commit()
    return {'message':'Visit {visit_id} deleted successfully'}

@app.post('/appointments')
def add_appointment(appointment:AppointmentsSchema, session: Session = Depends(get_db)):
    #create an instance model of the visits
    new_appointment = Appointment(**appointment.model_dump())
    #add the visit
    session.add(new_appointment)
    #commit visit to the db
    session.commit()
    session.refresh(new_appointment)
    return {'message':'appointment added successfully'}

@app.patch('/appointments/{appointment_id}')
def update_appointment(appointment_id: int, appointment=AppointmentsSchema, session: Session = Depends(get_db)):
    appointment = session.query(Appointment).filter(Appointment.id == appointment_id).first()
    #patch the appt
    #commit the visit to the db
    session.commit()
    session.refresh(appointment)
    return {'message':'appointment {appointment.id} fixed'}

@app.delete('/appointments/{id}')
def delete_appointment(appointment_id:int, session: Session = Depends(get_db)):
    #delete an appointment
    appointment = session.query(Appointment).filter(Appointment.id == appointment_id).first()
    #to commit the delee    
    session.delete(appointment)
    session.commit()
    return {
        "message": "Appointment deleted successfully",
        "appointment_id": appointment_id
    }
@app.get('/doctors')
def get_all_doctors(doctor_id: int, session: Session = Depends(get_db)):
    #gfet all doctors
    doctor = session.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Doctor with id {doctor_id} not found"
        )
    return doctor

@app.post('/doctors/{doctor_id}')
def add_doctor(doctor: DoctorsSchema, session: Session = Depends(get_db)):
    # add a new doctor to the db
    new_doctor = Doctor(**doctor.model_dump())
    session.add(new_doctor)
    session.commit()
    session.refresh(new_doctor)
    return {'message':'Doctor {new_doctor.id} has been added successfully!'}

@app.delete('/doctors/{doctor_id}')
def delete_doctor(doctor_id:int, session: Session = Depends(get_db)):
    # delete a doctorfrom the db
    doctor = session.query(Doctor).filter(Doctor.id == doctor_id).first()
    session.delete(doctor)
    #commit the delete
    session.commit()
    return {'message':'doctor {doctor_id} deleted successfully'}




