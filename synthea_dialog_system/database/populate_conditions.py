import json
from typing import Optional

from sqlalchemy.orm import Session

from ..logging import LOGGER
from . import ENGINE, FILES, SYNTHEA_FOLDER
from .tables import Condition


def load_bundle_files() -> list[dict]:
    """Loads the sample files"""
    condition_resources_list = []

    for file in FILES:
        with open(f"{SYNTHEA_FOLDER}/{file}", "r") as f:
            resource_bundle = json.loads(f.read())

        condition_resources = filter_condition_resource(resource_bundle=resource_bundle)
        if condition_resources is None:
            continue

        condition_resources_list.extend(condition_resources)

    return condition_resources_list


def filter_condition_resource(resource_bundle: dict) -> Optional[list[dict]]:
    """Filters out the conditions resource from the bundle resource"""
    candidates = [
        entry["resource"]
        for entry in resource_bundle["entry"]
        if entry["resource"]["resourceType"] == "Condition"
    ]

    if len(candidates) < 1:
        return None

    return candidates


def create_condition_entity(condition_resource: dict) -> Condition:
    """Creates a Condition entity from a condition resource"""
    condition_id = condition_resource["id"]
    name = condition_resource["code"]["coding"][0]["display"]
    clinical_status = condition_resource["clinicalStatus"]["coding"][0]["code"]
    category = condition_resource["category"][0]["coding"][0]["display"]
    subject = condition_resource["subject"]["reference"][9:]
    onset_datetime = condition_resource["onsetDateTime"]
    abatement_datetime = (
        condition_resource["abatementDateTime"]
        if "abatementDateTime" in condition_resource.keys()
        else None
    )
    recorded_date = condition_resource["recordedDate"]

    return Condition(
        condition_id=condition_id,
        name=name,
        clinical_status=clinical_status,
        category=category,
        subject=subject,
        onset_datetime=onset_datetime,
        abatement_datetime=abatement_datetime,
        recorded_date=recorded_date,
    )


def extract_condition_entities(condition_resources: list[dict]) -> list[Condition]:
    """Extracts a list of ConditionCode from the condition resources"""
    condition_entities = []

    for condition_resource in condition_resources:
        condition_entity = create_condition_entity(
            condition_resource=condition_resource
        )
        condition_entities.append(condition_entity)

    return condition_entities


def insert_entities(entities: list[Condition]):
    """Stores the list of entities into the database"""
    with Session(ENGINE) as session:
        session.add_all(entities)

        session.commit()


def run_conditions():
    """Runs the pipeline to insert patients into the DB"""
    LOGGER.info("Starting conditions insertion into DB.")

    LOGGER.info("Loading sample files.")
    condition_resources_list = load_bundle_files()

    LOGGER.info("Extracting condition entities from condition resources.")
    condition_entities = extract_condition_entities(
        condition_resources=condition_resources_list
    )

    LOGGER.info(f"Inserting {len(condition_entities)} Condition into DB.")
    insert_entities(entities=condition_entities)

    LOGGER.info("Conditions insertion finished.")
