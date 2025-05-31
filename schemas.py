# this file contains classes acting as blueprints for post/patch methods
from pydantic import BaseModel
from sqlalchemy import Date, Text

class PatientsSchema(BaseModel):
    name: str
    age: int
    phone_number: int
    address: str
    account_types: str
    
class DoctorsSchema(BaseModel):
    name: str

class VisitsSchema(BaseModel):
    date: Date
    summary : str
    procedure_details: str
    amount_paid: int
    balance: int
    doctor_id: str
    patient_id: str

class AppointmentsSChema(BaseModel):
    date: Date
    patient_id: int
    doctor_id: int

class PrescriptionsSchema(BaseModel):
    details: Text
    visit_id: int
