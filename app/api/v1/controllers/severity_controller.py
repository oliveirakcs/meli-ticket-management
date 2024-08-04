"""Severity Controller"""

from typing import List
from pydantic import UUID4
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Depends
from app.infrastructure import get_db, Severity
from app.schemas import Severity as SchemaSeverity, SeverityUpdate as SchemaSeverityUpdate


class SeverityController:
    """
    A controller class for managing severity operations in the database.
    """

    def __init__(self, db: Session):
        """
        Initialize the SeverityController with a database session.

        Args:
            db (Session): The database session.
        """
        self.db = db

    def get_all(self) -> List[SchemaSeverity]:
        """
        Get all severity levels.

        Returns:
            List[SchemaSeverity]: A list of severity objects.

        Raises:
            HTTPException: Raised if no severity levels are found.
        """
        severities = self.db.query(Severity).all()
        if not severities:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No severity levels found")
        return severities

    def create(self, request: Severity) -> Severity:
        """
        Create a new severity level.

        Args:
            request (Severity): The request containing details of the new severity level.

        Returns:
            Severity: The newly created severity object.

        Raises:
            HTTPException: Raised if any required field is not provided or if a severity with the same level already exists.
        """
        if request.level == 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Severity level 1 is handled by another team. Please contact the dedicated support team.",
            )

        existing_severity = self.db.query(Severity).filter_by(level=request.level).first()
        if existing_severity:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"A severity with level '{request.level}' already exists.",
            )

        new_severity = Severity(level=request.level, description=request.description)

        self.db.add(new_severity)
        self.db.commit()
        self.db.refresh(new_severity)

        return new_severity

    def show(self, severity_id: UUID4) -> SchemaSeverity:
        """
        Retrieve a severity level by severity ID.

        Args:
            severity_id (UUID4): The ID of the severity to retrieve.

        Returns:
            Severity: The severity corresponding to the provided ID.

        Raises:
            HTTPException: Raised if the severity with the provided ID is not found.
        """
        severity = self.db.query(Severity).filter(Severity.id == severity_id).first()
        if not severity:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Severity {severity_id} not found",
            )
        return severity

    def update(self, severity_id: UUID4, request: SchemaSeverityUpdate) -> SchemaSeverity:
        """
        Update severity information.

        Args:
            severity_id (UUID4): The ID of the severity to update.
            request (SeverityUpdate): The updated severity information.

        Returns:
            Severity: The updated severity information.

        Raises:
            HTTPException: Raised if the severity with the provided ID is not found or if any field is invalid.
        """
        severity = self.db.query(Severity).filter(Severity.id == severity_id).first()
        if not severity:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Severity {severity_id} not found",
            )

        if request.level is not None and request.level != severity.level:
            existing_severity = self.db.query(Severity).filter_by(level=request.level).first()
            if existing_severity:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"A severity with level '{request.level}' already exists.",
                )

        for key, value in request.dict(exclude_unset=True).items():
            setattr(severity, key, value)

        self.db.commit()
        self.db.refresh(severity)
        return severity

    def delete(self, severity_id: UUID4) -> str:
        """
        Delete a severity level by severity UUID.

        Args:
            severity_id (UUID4): The ID of the severity to be deleted.

        Returns:
            str: A message confirming the deletion of the severity level.

        Raises:
            HTTPException: Raised if the severity with the provided ID is not found.
        """
        severity = self.db.query(Severity).filter(Severity.id == severity_id).first()
        if not severity:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Severity {severity_id} not found")

        self.db.delete(severity)
        self.db.commit()
        return f"Severity {severity_id} deleted."


def get_severity_controller(db: Session = Depends(get_db)):
    """
    Dependency to get an instance of SeverityController.

    Args:
        db (Session): The database session.

    Returns:
        SeverityController: An instance of SeverityController.
    """
    return SeverityController(db=db)
