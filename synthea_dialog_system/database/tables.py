from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Patient(Base):
    __tablename__ = "patient"
    patient_id: Mapped[UUID] = mapped_column(primary_key=True)
    active: Mapped[bool]
    given_name: Mapped[Optional[str]]
    family_name: Mapped[Optional[str]]
    telecom: Mapped[Optional[str]]
    gender: Mapped[Optional[str]]
    birth_date: Mapped[datetime]
    deceased_boolean: Mapped[bool]
    deceased_datetime: Mapped[datetime]
    address: Mapped[Optional[str]]
    marital_status: Mapped[Optional[str]]
    language: Mapped[Optional[str]]

    def __repr__(self) -> str:
        return f"Patient({self.family_name}, {self.given_name})"


class Condition(Base):
    __tablename__ = "condition"
    condition_id: Mapped[UUID] = mapped_column(primary_key=True)
    name: Mapped[Optional[str]]
    clinical_status: Mapped[Optional[str]]
    category: Mapped[Optional[str]]
    subject: Mapped[UUID] = mapped_column(ForeignKey("patient.patient_id"))
    onset_datetime: Mapped[datetime]
    abatement_datetime: Mapped[datetime]
    recorded_date: Mapped[datetime]

    def __repr__(self) -> str:
        return f"Condition({self.name})"
