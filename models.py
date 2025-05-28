from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Date, String, Float, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import date


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
    appointments = relationship("Appointments", back_populates="patient")

class Doctor(Base):
    __tablename__ = 'doctors'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    visits = relationship("Visit", back_populates="doctor")
    appointments = relationship("Appointments", back_populates="doctor")

class Visit(Base):
    __tablename__ = 'visits'
    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False, default=date.today)
    summary = Column(String, nullable=False)
    procedure_details = Column(Text, nullable=False)
    amount_paid = Column(Float, nullable=False)
    balance = Column(Float, nullable=True)
    doctor_id = Column(Integer, ForeignKey('doctors.id'))
    patient_id = Column(Integer, ForeignKey('patients.id'))
    patient = relationship("Patient", back_populates="visit")
    doctor = relationship("Doctor", back_populates="visits")
    prescription = relationship("Prescription", back_populates="visits")

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