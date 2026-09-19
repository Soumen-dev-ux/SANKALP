import sys
from pathlib import Path

# Add apps/api directory to sys.path so python scripts/seed_demo.py works directly
API_DIR = Path(__file__).resolve().parents[1]
if str(API_DIR) not in sys.path:
    sys.path.insert(0, str(API_DIR))

import json
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.region import Region
from app.models.demographic import Demographic
from app.models.infrastructure import Infrastructure
from app.models.government_project import GovernmentProject
from app.models.citizen_request import CitizenRequest
from app.services.data_ingestion_service import (
    ingest_demographic,
    ingest_infrastructure,
    ingest_project,
)

BASE_DIR = Path(__file__).resolve().parents[3]
SEED_DIR = BASE_DIR / "data" / "seed"


def load_json(filename: str):
    path = SEED_DIR / filename
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def reset_and_seed_regions(db: Session):
    records = load_json("regions.json")
    valid_ids = [r["id"] for r in records]

    # Handle references
    db.query(CitizenRequest).filter(~CitizenRequest.region_id.in_(valid_ids)).update(
        {CitizenRequest.region_id: None}, synchronize_session=False
    )

    inserted = 0
    skipped = 0

    for data in records:
        existing = db.query(Region).filter(Region.id == data["id"]).first()
        if existing:
            existing.name = data["name"]
            if "code" in data:
                existing.code = data["code"]
            inserted += 1
        else:
            region = Region(
                id=data["id"],
                name=data["name"],
                code=data.get("code"),
            )
            db.add(region)
            inserted += 1
    db.commit()
    return inserted, skipped


def seed_demographics_summary(db: Session):
    records = load_json("demographics.json")
    db.query(Demographic).delete(synchronize_session=False)
    db.commit()

    inserted = 0
    skipped = 0
    for data in records:
        res = ingest_demographic(db, data)
        if res.startswith("Inserted"):
            inserted += 1
        else:
            skipped += 1
    db.commit()
    return inserted, skipped


def seed_infrastructure_summary(db: Session):
    records = load_json("infrastructure.json")
    db.query(Infrastructure).delete(synchronize_session=False)
    db.commit()

    inserted = 0
    skipped = 0
    for data in records:
        res = ingest_infrastructure(db, data)
        if res.startswith("Inserted"):
            inserted += 1
        else:
            skipped += 1
    db.commit()
    return inserted, skipped


def seed_projects_summary(db: Session):
    records = load_json("government_projects.json")
    db.query(GovernmentProject).delete(synchronize_session=False)
    db.commit()

    inserted = 0
    skipped = 0
    for data in records:
        res = ingest_project(db, data)
        if res.startswith("Inserted"):
            inserted += 1
        else:
            skipped += 1
    db.commit()
    return inserted, skipped


def main():
    db = SessionLocal()
    try:
        print("Starting SANKALP demo data ingestion...\n")

        r_ins, r_skip = reset_and_seed_regions(db)
        print(f"Regions: inserted={r_ins}, skipped={r_skip}")

        d_ins, d_skip = seed_demographics_summary(db)
        print(f"Demographics: inserted={d_ins}, skipped={d_skip}")

        i_ins, i_skip = seed_infrastructure_summary(db)
        print(f"Infrastructure: inserted={i_ins}, skipped={i_skip}")

        p_ins, p_skip = seed_projects_summary(db)
        print(f"Government projects: inserted={p_ins}, skipped={p_skip}")

        print("\nDemo data ingestion completed successfully.")
    finally:
        db.close()


if __name__ == "__main__":
    main()