from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Date, String, Float, Text, ForeignKey, create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker

#1. create the engine that connects the db
engine = create_engine('sqlite:///clinic.db', echo=True)

#2. create a session
Session = sessionmaker(bind=engine)

# 3. for fastapi, we need to create a method/ function that returns the session
def get_db():
    session = Session()
    try:
        yield session
    finally:
        session.close()


Base = declarative_base()

class Patient(Base):
    __tablename__ = 'patients'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    phone_number = Column(Integer, nullable=False)
    address = Column(String, nullable=False)
    account_type = Column(String, nullable=False)
    visits = relationship("Visit", back_populates="patient")
    appointments = relationship("Appointment", back_populates="patient")

class Doctor(Base):
    __tablename__ = 'doctors'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    visits = relationship("Visit", back_populates="doctor")
    appointments = relationship("Appointment", back_populates="doctor")

class Visit(Base):
    __tablename__ = 'visits'
    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    summary = Column(String, nullable=False)
    procedure_details = Column(Text, nullable=False)
    amount_paid = Column(Float, nullable=False)
    balance = Column(Float, nullable=True)
    doctor_id = Column(Integer, ForeignKey('doctors.id'))
    patient_id = Column(Integer, ForeignKey('patients.id'))
    patient = relationship("Patient", back_populates="visits")
    doctor = relationship("Doctor", back_populates="visits")
    prescription = relationship("Prescription", back_populates="visit")

class Appointment(Base):
    __tablename__ = 'appointments'
    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    patient_id = Column(Integer, ForeignKey('patients.id'))
    doctor_id = Column(Integer, ForeignKey('doctors.id'))
    patient = relationship("Patient", back_populates="appointments")
    doctor = relationship("Doctor", back_populates="appointments")

class Prescription(Base):
    __tablename__ = 'prescriptions'
    id = Column(Integer, primary_key=True)
    details = Column(Text, nullable=False)
    visit_id = Column(Integer, ForeignKey('visits.id'))
    visit = relationship("Visit", back_populates="prescriptions")

Base.metadata.create_all(bind=engine)