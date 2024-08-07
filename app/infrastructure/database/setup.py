"""Create initial tables in the database."""

import os
from app.core import TicketStatus
from app.infrastructure.database.models import User, Severity, Category, Subcategory, Ticket, TicketCategory, TicketSubcategory
from app.infrastructure.database import SessionLocal
from app.core.auth.hashing import Hash
from app.infrastructure.database import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER

db = SessionLocal()

connection_string = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

"""This module provides functions to create initial tables and records in the database."""


def create_sysadmin():
    """Create the sysadmin user if it does not exist.

    This function checks if the sysadmin user exists in the database.
    If not, it creates the sysadmin user.
    """

    user = db.query(User).filter(User.username == "sysadmin").first()

    if not user:
        new_user = User(
            username=os.environ["SYSADMIN_USERNAME"],
            name=os.environ["SYSADMIN_NAME"],
            email=os.environ["SYSADMIN_EMAIL"],
            password=Hash.bcrypt(os.environ["SYSADMIN_PASSWORD"]),
            active=True,
            role="sysadmin",
        )
        db.add(new_user)
        db.commit()
        print("Sysadmin user created!")


def create_severities():
    """Create initial severity levels if they do not exist.

    This function checks if severity levels exist in the database.
    If not, it creates the severity levels: 1 = issue high, 2 = high, 3 = medium, 4 = low.
    """

    existing_severities = db.query(Severity).count()

    if existing_severities == 0:
        severities = [
            Severity(level=1, description="Issue High"),
            Severity(level=2, description="High"),
            Severity(level=3, description="Medium"),
            Severity(level=4, description="Low"),
        ]

        db.add_all(severities)
        db.commit()
        print("Severities created!")


def create_categories():
    """Create initial categories if they do not exist.

    This function checks if categories exist in the database.
    If not, it creates the initial categories: Deploy, Development, Infrastructure, Testing, and more.
    """

    existing_categories = db.query(Category).count()

    if existing_categories == 0:
        categories = [
            Category(name="Deploy"),
            Category(name="Development"),
            Category(name="Infrastructure"),
            Category(name="Testing"),
            Category(name="Security"),
            Category(name="Operations"),
            Category(name="Monitoring"),
            Category(name="Database Management"),
            Category(name="Networking"),
            Category(name="User Experience"),
        ]

        db.add_all(categories)
        db.commit()
        print("Categories created!")


def create_fake_tickets():
    """Create fake tickets for testing purposes."""

    existing_tickets = db.query(Ticket).count()

    if existing_tickets == 0:

        development_category = db.query(Category).filter(Category.name == "Development").first()
        testing_category = db.query(Category).filter(Category.name == "Testing").first()
        deploy_category = db.query(Category).filter(Category.name == "Deploy").first()

        development_subcategories = db.query(Subcategory).filter(Subcategory.category_id == development_category.id).all()
        testing_subcategories = db.query(Subcategory).filter(Subcategory.category_id == testing_category.id).all()
        deploy_subcategories = db.query(Subcategory).filter(Subcategory.category_id == deploy_category.id).all()

        development_severity = db.query(Severity).filter(Severity.level == 2).first()
        testing_severity = db.query(Severity).filter(Severity.level == 3).first()
        deploy_severity = db.query(Severity).filter(Severity.level == 4).first()

        tickets = [
            Ticket(
                title="Ticket Test 1",
                description="This is a test ticket for development purposes.",
                severity_id=development_severity.id,
                status=TicketStatus.ABERTO,
            ),
            Ticket(
                title="Ticket Test 2",
                description="This is a test ticket for testing purposes.",
                severity_id=testing_severity.id,
                status=TicketStatus.EM_PROGRESSO,
            ),
            Ticket(
                title="Ticket Test 3",
                description="This is a test ticket for deployment purposes.",
                severity_id=deploy_severity.id,
                status=TicketStatus.RESOLVIDO,
            ),
        ]

        db.add_all(tickets)
        db.commit()

        for ticket in tickets:
            if ticket.title == "Ticket Test 1":
                db.add(TicketCategory(ticket_id=ticket.id, category_id=development_category.id))
                for subcategory in development_subcategories:
                    db.add(TicketSubcategory(ticket_id=ticket.id, subcategory_id=subcategory.id))

            elif ticket.title == "Ticket Test 2":
                db.add(TicketCategory(ticket_id=ticket.id, category_id=testing_category.id))
                for subcategory in testing_subcategories:
                    db.add(TicketSubcategory(ticket_id=ticket.id, subcategory_id=subcategory.id))

            elif ticket.title == "Ticket Test 3":
                db.add(TicketCategory(ticket_id=ticket.id, category_id=deploy_category.id))
                for subcategory in deploy_subcategories:
                    db.add(TicketSubcategory(ticket_id=ticket.id, subcategory_id=subcategory.id))

        db.commit()
        print("Fake tickets created!")


def create_subcategories():
    """Create initial subcategories if they do not exist.

    This function checks if subcategories exist in the database.
    If not, it creates the initial subcategories under their respective categories.
    """

    deploy_category = db.query(Category).filter(Category.name == "Deploy").first()
    development_category = db.query(Category).filter(Category.name == "Development").first()
    infrastructure_category = db.query(Category).filter(Category.name == "Infrastructure").first()
    testing_category = db.query(Category).filter(Category.name == "Testing").first()
    security_category = db.query(Category).filter(Category.name == "Security").first()
    operations_category = db.query(Category).filter(Category.name == "Operations").first()
    monitoring_category = db.query(Category).filter(Category.name == "Monitoring").first()
    database_management_category = db.query(Category).filter(Category.name == "Database Management").first()
    networking_category = db.query(Category).filter(Category.name == "Networking").first()
    user_experience_category = db.query(Category).filter(Category.name == "User Experience").first()

    existing_subcategories = db.query(Subcategory).count()

    if existing_subcategories == 0:
        subcategories = []

        if deploy_category:
            subcategories.extend(
                [
                    Subcategory(name="CI/CD", category_id=deploy_category.id),
                    Subcategory(name="Circle CI", category_id=deploy_category.id),
                    Subcategory(name="Image Deployment", category_id=deploy_category.id),
                    Subcategory(name="Kubernetes", category_id=deploy_category.id),
                    Subcategory(name="Docker", category_id=deploy_category.id),
                    Subcategory(name="GitOps", category_id=deploy_category.id),
                ]
            )

        if development_category:
            subcategories.extend(
                [
                    Subcategory(name="Frontend Development", category_id=development_category.id),
                    Subcategory(name="Backend Development", category_id=development_category.id),
                    Subcategory(name="Mobile Development", category_id=development_category.id),
                    Subcategory(name="API Development", category_id=development_category.id),
                    Subcategory(name="DevOps", category_id=development_category.id),
                    Subcategory(name="Full Stack Development", category_id=development_category.id),
                ]
            )

        if infrastructure_category:
            subcategories.extend(
                [
                    Subcategory(name="Cloud Infrastructure", category_id=infrastructure_category.id),
                    Subcategory(name="On-premise Infrastructure", category_id=infrastructure_category.id),
                    Subcategory(name="Virtualization", category_id=infrastructure_category.id),
                    Subcategory(name="Infrastructure as Code", category_id=infrastructure_category.id),
                    Subcategory(name="Serverless Architecture", category_id=infrastructure_category.id),
                ]
            )

        if testing_category:
            subcategories.extend(
                [
                    Subcategory(name="Automated Testing", category_id=testing_category.id),
                    Subcategory(name="Manual Testing", category_id=testing_category.id),
                    Subcategory(name="Performance Testing", category_id=testing_category.id),
                    Subcategory(name="Security Testing", category_id=testing_category.id),
                    Subcategory(name="Unit Testing", category_id=testing_category.id),
                    Subcategory(name="Integration Testing", category_id=testing_category.id),
                ]
            )

        if security_category:
            subcategories.extend(
                [
                    Subcategory(name="Application Security", category_id=security_category.id),
                    Subcategory(name="Network Security", category_id=security_category.id),
                    Subcategory(name="Data Security", category_id=security_category.id),
                    Subcategory(name="Identity Management", category_id=security_category.id),
                    Subcategory(name="Threat Detection", category_id=security_category.id),
                ]
            )

        if operations_category:
            subcategories.extend(
                [
                    Subcategory(name="Incident Management", category_id=operations_category.id),
                    Subcategory(name="Change Management", category_id=operations_category.id),
                    Subcategory(name="Service Management", category_id=operations_category.id),
                    Subcategory(name="Release Management", category_id=operations_category.id),
                    Subcategory(name="Disaster Recovery", category_id=operations_category.id),
                ]
            )

        if monitoring_category:
            subcategories.extend(
                [
                    Subcategory(name="Application Monitoring", category_id=monitoring_category.id),
                    Subcategory(name="Infrastructure Monitoring", category_id=monitoring_category.id),
                    Subcategory(name="User Monitoring", category_id=monitoring_category.id),
                    Subcategory(name="Log Monitoring", category_id=monitoring_category.id),
                    Subcategory(name="Network Monitoring", category_id=monitoring_category.id),
                ]
            )

        if database_management_category:
            subcategories.extend(
                [
                    Subcategory(name="SQL Databases", category_id=database_management_category.id),
                    Subcategory(name="NoSQL Databases", category_id=database_management_category.id),
                    Subcategory(name="Database Design", category_id=database_management_category.id),
                    Subcategory(name="Database Optimization", category_id=database_management_category.id),
                    Subcategory(name="Data Warehousing", category_id=database_management_category.id),
                ]
            )

        if networking_category:
            subcategories.extend(
                [
                    Subcategory(name="LAN", category_id=networking_category.id),
                    Subcategory(name="WAN", category_id=networking_category.id),
                    Subcategory(name="Network Security", category_id=networking_category.id),
                    Subcategory(name="Network Architecture", category_id=networking_category.id),
                    Subcategory(name="Wireless Networking", category_id=networking_category.id),
                ]
            )

        if user_experience_category:
            subcategories.extend(
                [
                    Subcategory(name="UI/UX Design", category_id=user_experience_category.id),
                    Subcategory(name="Accessibility", category_id=user_experience_category.id),
                    Subcategory(name="User Research", category_id=user_experience_category.id),
                    Subcategory(name="Usability Testing", category_id=user_experience_category.id),
                    Subcategory(name="Interaction Design", category_id=user_experience_category.id),
                ]
            )
        db.add_all(subcategories)
        db.commit()
        print("Subcategories created!")
