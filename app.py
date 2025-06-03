#Import fastapi packages
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from schemas import PatientsSchema, VisitsSchema, DoctorsSchema, AppointmentsSchema, PrescriptionSchema
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

#======here we define the patient endpoints ========
# http://localhost:8000/patients -> GETs a single patient
# @app.get('/patients')
# def all_patients(session: Session = Depends(get_db)):
#     #sqlalchemy retrieves all patients from the table
#     all_patients = session.query(Patient).all()
#     return all_patients

@app.get('/patients')
def get_all_patients(session: Session = Depends(get_db)):
    #to get ALL patients from the db
    patients = session.query(Patient).all()
    print("Patient id", id)
    return patients

@app.get('/patients/{patient_id}', response_model=PatientsSchema)
def get_patient(patient_id: int, session: Session = Depends(get_db)):
    # get patient by id
    patient = session.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_Not_Found,
            detail= f"Patient with ID {patient_id} not found"
        )
    return patient

@app.get('/patients/{patient_id}/visits')
def get_patient_visits(patient_id: int, session: Session = Depends(get_db)):
    patient = session.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Patient with ID {patient_id} not found"
        )
    return patient.visits # SQLAlchemy's relationship allows us to get the patients visits by id

@app.get('/patients/{patient_id}/appointments')
def get_patient_appointments(patient_id: int, session: Session = Depends(get_db)):
    patient = session.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Patient with ID {patient_id} not found"
        )
    return patient.appointments # SQLAlchemy's relationship gets us the appointments for this patient id
    

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
def update_patient(patient_id:int, patient:PatientsSchema, session: Session = Depends(get_db)):
    # update patients' info
    patient = session.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_400_NOT_FOUND,
            detail= f"Patient with ID {patient_id} not found!"
        )
    #update only fields from the request
    update_data = patient.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(patient, field, value)
    # commit the seesion
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

@app.get('/visits/{visit_id}/prescriptions')
def get_visit_prescriptions(visit_id: int, session: Session = Depends(get_db)):
    visit = session.query(Visit).filter(Visit.id == visit_id).first()
    if not visit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Visit with ID {visit_id} not found"
        )
    return visit.prescription #to take advantage of list/relationship

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
def update_visit(visit_id: int, visit: VisitsSchema, session: Session = Depends(get_db)):
    #get a visit by id
    visit = session.query(Visit).filter(Visit.id == visit_id).first()
    if not visit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Visit with id {visit_id} not found"
        )
    # Update only the fields that are provided in the request
    update_data = visit.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(visit, field, value)

    #add the visit
    #commit visit to the db
    session.commit()
    session.refresh(visit)
    return {'message':'Visit {visit.id} added successfully'}

@app.delete('/visits/{visit_id}')
def delete_visit(visit_id:int, session: Session = Depends(get_db)):
    #delete the visit from the db
    visit = session.query(Visit).filter(Visit.id == visit_id).first()
    if not visit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Visit with id {visit_id} not found"
        )
    
    session.delete(visit)
    #commit the delete
    session.commit()
    return {'message':'Visit {visit_id} deleted successfully'}

#======appointntment endpoints===========
@app.get('/appointments')
def get_all_appointments(session: Session = Depends(get_db)):
    appointments = session.query(Appointment).all()
    return appointments

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
    # Update only the fields that are provided in the request
    update_data = appointment.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(appointment, field, value)
    
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

#=======doctor endpoints========

@app.get('/doctors') # This will now be for getting all doctors
def get_all_doctors(session: Session = Depends(get_db)):
    all_doctors = session.query(Doctor).all()
    return all_doctors

@app.get('/doctors{doctor_id}')
def get_doctor_by_id(doctor_id: int, session: Session = Depends(get_db)):#this will get
    #gfet all doctors
    doctor = session.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Doctor with id {doctor_id} not found"
        )
    return doctor

@app.post('/doctors')
def add_doctor(doctor: DoctorsSchema, session: Session = Depends(get_db)):
    # add a new doctor to the db
    new_doctor = Doctor(**doctor.model_dump())
    session.add(new_doctor)
    session.commit()
    session.refresh(new_doctor)
    return {'message':'Doctor {new_doctor.id} has been added successfully!'}

@app.patch('/doctors/{doctor_id}')
def update_doctor(doctor_id: int, doctor: DoctorsSchema, session: Session = Depends(get_db)):
    #update an existing doctor's info
    doctor = session.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Doctor with id {doctor_id} not found"
        )

@app.delete('/doctors/{doctor_id}')
def delete_doctor(doctor_id:int, session: Session = Depends(get_db)):
    # delete a doctorfrom the db
    doctor = session.query(Doctor).filter(Doctor.id == doctor_id).first()
    session.delete(doctor)
    #commit the delete
    session.commit()
    return {'message':'doctor {doctor_id} deleted successfully'}

# ========== PRESCRIPTION ENDPOINTS ==========
@app.get('/prescriptions')
#get all prescriptions
def get_all_prescriptions(session: Session = Depends(get_db)):
    """Get all prescriptions from the database"""
    prescriptions = session.query(Prescription).all()
    return prescriptions

@app.get('/prescriptions/{prescription_id}', prescription=PrescriptionSchema)
def get_prescription(prescription_id: int, session: Session = Depends(get_db)):
    """Get a single prescription by ID"""
    prescription = session.query(Prescription).filter(Prescription.id == prescription_id).first()
    if not prescription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Prescription with id {prescription_id} not found"
        )
    return prescription

@app.post('/prescriptions')
def add_prescription(prescription: PrescriptionSchema, session: Session = Depends(get_db)):
    """Add a new prescription to the database"""
    # Check if prescription exists
    visit = session.query(Visit).filter(Visit.id == prescription.visit_id).first()
    if not visit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Visit with id {prescription.visit_id} not found"
        )
    
    new_prescription = Prescription(**prescription.model_dump())
    session.add(new_prescription)
    session.commit()
    session.refresh(new_prescription)
    return {
        "message": "Prescription created successfully",
        "prescription_id": new_prescription.id
    }

@app.patch('/prescriptions/{prescription_id}')
def update_prescription(prescription_id: int, prescription_data: PrescriptionSchema, session: Session = Depends(get_db)):
    """Update an existing prescription's information"""
    prescription = session.query(Prescription).filter(Prescription.id == prescription_id).first()
    if not prescription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Prescription with id {prescription_id} not found"
        )
    
    # Update only the fields that are provided in the request
    update_data = prescription_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(prescription, field, value)
    
    session.commit()
    session.refresh(prescription)
    return {
        "message": "Prescription updated successfully",
        "prescription_id": prescription.id
    }

@app.delete('/prescriptions/{prescription_id}')
def delete_prescription(prescription_id: int, session: Session = Depends(get_db)):
    """Delete a prescription from the database"""
    prescription = session.query(Prescription).filter(Prescription.id == prescription_id).first()
    if not prescription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Prescription with id {prescription_id} not found"
        )
    
    session.delete(prescription)
    session.commit()
    return {
        "message": "Prescription deleted successfully",
        "prescription_id": prescription_id
    }




