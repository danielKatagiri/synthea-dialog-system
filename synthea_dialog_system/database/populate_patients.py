import json
from typing import Optional

from sqlalchemy.orm import Session

from ..logging import LOGGER
from . import ENGINE, FILES, SYNTHEA_FOLDER
from .tables import Patient


def filter_patient_resource(resource_bundle: dict) -> Optional[dict]:
    """Filters out the patient resource from the bundle resource"""
    candidates = [
        entry["resource"]
        for entry in resource_bundle["entry"]
        if entry["resource"]["resourceType"] == "Patient"
    ]

    if len(candidates) < 1:
        return None

    return candidates[0]


def create_patient_entity(patient_resource: dict) -> Patient:
    """Creates a Patient entity from a patient resource"""

    patient_id = patient_resource["id"]
    given_name = " ".join(patient_resource["name"][0]["given"])
    family_name = patient_resource["name"][0]["family"]
    telecom = patient_resource["telecom"][0]["value"]
    gender = patient_resource["gender"]
    birth_date = patient_resource["birthDate"]

    deceased_boolean = (
        patient_resource["deceasedBoolean"]
        if "deceasedBoolean" in patient_resource.keys()
        else False
    )
    deceased_datetime = (
        patient_resource["deceasedDateTime"]
        if "deceasedDateTime" in patient_resource.keys()
        else None
    )

    address = f"{patient_resource['address'][0]['line'][0], patient_resource['address'][0]['city']}, {patient_resource['address'][0]['state']}"
    marital_status = patient_resource["maritalStatus"]["text"]
    language = patient_resource["communication"][0]["language"]["text"]

    patient = Patient(
        patient_id=patient_id,
        given_name=given_name,
        family_name=family_name,
        telecom=telecom,
        gender=gender,
        birth_date=birth_date,
        deceased_boolean=deceased_boolean,
        deceased_datetime=deceased_datetime,
        address=address,
        marital_status=marital_status,
        language=language,
    )

    return patient


def run_patients():
    """Runs the pipeline to insert patients into the DB"""
    LOGGER.info("Starting patients insertion into DB.")

    patients = []

    LOGGER.info("Loading sample files.")
    for file in FILES:
        with open(f"{SYNTHEA_FOLDER}/{file}", "r") as f:
            resource_bundle = json.loads(f.read())

        patient_resource = filter_patient_resource(resource_bundle=resource_bundle)
        if patient_resource is None:
            continue

        patient_entity = create_patient_entity(patient_resource=patient_resource)
        patients.append(patient_entity)

    LOGGER.info(f"Found {len(patients)} patients.")

    LOGGER.info("Inserting into DB.")
    with Session(ENGINE) as session:
        session.add_all(patients)

        session.commit()
        LOGGER.info("Insertion finished.")

    LOGGER.info("Patients insertion finished.")
