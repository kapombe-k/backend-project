# this file contains classes acting as blueprints for post/patch methods
from pydantic import BaseModel

class PatientsSchema(BaseModel):
    name: str
    age: int
    phone_number: int
    address: str
    account_types: str
    
class DoctorsSchema(BaseModel):
    name: str

class VisitsSchema(BaseModel):
    summary : str
    procedure_details: str
    amount_paid: int
    balance: int
    doctor_id: str
    patient_id: str

class AppointmentsSchema(BaseModel):
    patient_id: int
    doctor_id: int

