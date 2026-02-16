from app import app
from extensions import db
from models import Room


with app.app_context():

    room1 = Room(
        name="Deluxe Room",
        price=2000,
        image="room1.jpg"
    )

    room2 = Room(
        name="Luxury Room",
        price=3500,
        image="room2.jpg"
    )

    room3 = Room(
        name="Suite Room",
        price=5000,
        image="room3.jpg"
    )

    db.session.add_all([room1, room2, room3])
    db.session.commit()

    print("Rooms Added Successfully!")
