from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.hcp import HCP


class HCPRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_hcps(self) -> list[HCP]:
        return list(self.db.scalars(select(HCP).order_by(HCP.full_name)).all())

    def get_by_id(self, hcp_id: int) -> HCP | None:
        return self.db.get(HCP, hcp_id)

    def seed_if_empty(self) -> None:
        existing = self.db.scalars(select(HCP)).first()
        if existing:
            return

        demo_hcps = [
            HCP(
                full_name="Dr. Aisha Menon",
                specialty="Cardiology",
                hospital_name="Apollo Heart Institute",
                city="Hyderabad",
                tier="A",
                preferred_channel="In-person",
                notes="High-potential HCP, interested in long-term outcome data.",
            ),
            HCP(
                full_name="Dr. Raghav Sharma",
                specialty="Diabetology",
                hospital_name="Care Specialty Clinic",
                city="Bengaluru",
                tier="B",
                preferred_channel="Phone",
                notes="Requests concise scientific updates and patient adherence data.",
            ),
        ]
        self.db.add_all(demo_hcps)
        self.db.commit()
