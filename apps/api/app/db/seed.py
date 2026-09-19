import logging
import uuid
from sqlalchemy.orm import Session

from app.db.session import SessionLocal, engine
from app.db.base import Base
from app.models.region import Region
from app.models.citizen_request import CitizenRequest

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("seed")


def seed_db(db: Session) -> None:
    # Ensure tables exist
    Base.metadata.create_all(bind=engine)

    # Seed Regions if empty
    if db.query(Region).count() == 0:
        logger.info("Seeding regions...")
        
        # Level 1: Country
        ind = Region(code="IND", name="India", country_code="IN")
        db.add(ind)
        db.flush()

        # Level 2: States
        mh = Region(code="IND-MH", name="Maharashtra", country_code="IN", parent_region_id=ind.id)
        dl = Region(code="IND-DL", name="Delhi", country_code="IN", parent_region_id=ind.id)
        ka = Region(code="IND-KA", name="Karnataka", country_code="IN", parent_region_id=ind.id)
        db.add_all([mh, dl, ka])
        db.flush()

        # Level 3: Cities
        mum = Region(code="IND-MH-MUM", name="Mumbai", country_code="IN", parent_region_id=mh.id)
        blr = Region(code="IND-KA-BLR", name="Bengaluru", country_code="IN", parent_region_id=ka.id)
        db.add_all([mum, blr])
        db.flush()
        db.commit()
        logger.info("Regions seeded successfully.")
    else:
        logger.info("Regions table already has data. Skipping region seed.")

    # Seed Citizen Requests if empty
    if db.query(CitizenRequest).count() == 0:
        logger.info("Seeding citizen requests...")
        
        mum_region = db.query(Region).filter(Region.code == "IND-MH-MUM").first()
        blr_region = db.query(Region).filter(Region.code == "IND-KA-BLR").first()
        dl_region = db.query(Region).filter(Region.code == "IND-DL").first()

        sample_requests = [
            CitizenRequest(
                anonymous_reference=f"SANKALP-{uuid.uuid4().hex[:10].upper()}",
                raw_text="The main road near Ward 12 has multiple potholes causing heavy traffic congestion.",
                language="en",
                category="Infrastructure",
                intent="Road Repair",
                issue="Potholes & Traffic",
                region_id=mum_region.id if mum_region else None,
                latitude=19.0760,
                longitude=72.8777,
                status="submitted",
                source="web",
            ),
            CitizenRequest(
                anonymous_reference=f"SANKALP-{uuid.uuid4().hex[:10].upper()}",
                raw_text="Garbage has not been collected in Sector 4 for 3 days.",
                language="en",
                category="Sanitation",
                intent="Waste Collection",
                issue="Uncollected Garbage",
                region_id=blr_region.id if blr_region else None,
                latitude=12.9716,
                longitude=77.5946,
                status="submitted",
                source="web",
            ),
            CitizenRequest(
                anonymous_reference=f"SANKALP-{uuid.uuid4().hex[:10].upper()}",
                raw_text="Water supply disruption in Anand Nagar since yesterday morning.",
                language="en",
                category="Utilities",
                intent="Water Supply",
                issue="Water Disruption",
                region_id=dl_region.id if dl_region else None,
                latitude=28.6139,
                longitude=77.2090,
                status="submitted",
                source="web",
            ),
            CitizenRequest(
                anonymous_reference=f"SANKALP-{uuid.uuid4().hex[:10].upper()}",
                raw_text="Streetlights on Park Street are non-functional at night.",
                language="en",
                category="Infrastructure",
                intent="Street Lighting",
                issue="Defective Streetlights",
                region_id=mum_region.id if mum_region else None,
                latitude=19.0176,
                longitude=72.8561,
                status="submitted",
                source="mobile_app",
            ),
        ]

        db.add_all(sample_requests)
        db.commit()
        logger.info("Citizen requests seeded successfully.")
    else:
        logger.info("Citizen requests table already has data. Skipping citizen requests seed.")


def run_seed() -> None:
    db = SessionLocal()
    try:
        seed_db(db)
    finally:
        db.close()


if __name__ == "__main__":
    run_seed()
