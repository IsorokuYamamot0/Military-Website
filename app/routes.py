from app import app, db
from app.models import Tank, Plane


def populate_database():
    """Populates the database with sample data if it's empty."""
    print("Checking database...")
    # Add data only if the tables are empty
    if Tank.query.first() is None and Plane.query.first() is None:
        print("Database is empty. Populating with sample USA vehicles...")
        tanks_data = [
            {'name': 'M1 Abrams', 'year_introduced': 1980, 'description': 'The main battle tank of the United States Army and Marine Corps.'},
            {'name': 'M2 Bradley', 'year_introduced': 1981, 'description': 'An infantry fighting vehicle that serves as both a transport and a support vehicle.'}
        ]
        planes_data = [
            {'name': 'F-22 Raptor', 'role': 'Stealth Air Superiority Fighter', 'description': 'A fifth-generation, single-seat, twin-engine, all-weather stealth tactical fighter aircraft.'},
            {'name': 'B-2 Spirit', 'role': 'Stealth Bomber', 'description': 'A multi-role bomber capable of deploying both conventional and nuclear munitions.'},
            {'name': 'A-10 Thunderbolt II', 'role': 'Close Air Support', 'description': 'A single-seat, twin-turbofan engine, straight-wing jet aircraft developed for close air support.'}
        ]

        for data in tanks_data:
            db.session.add(Tank(**data))
        for data in planes_data:
            db.session.add(Plane(**data))
        db.session.commit()
        print("Database population complete.")
    else:
        print("Database already contains data. Skipping population.")


if __name__ == '__main__':
    # Use app_context to create database tables and populate them
    with app.app_context():
        db.create_all()
        populate_database()
    # Run the Flask development server
    app.run(debug=True)
