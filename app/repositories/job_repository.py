from sqlalchemy.orm import Session

from app.models.jobs import Job


class JobRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, job: Job) -> Job:
        try:
            self.db.add(job)
            self.db.commit()
            self.db.refresh(job)
            return job
        except Exception:
            self.db.rollback()
            raise