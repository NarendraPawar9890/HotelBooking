from flask import Flask, render_template, redirect,request, url_for, flash
from werkzeug.security import generate_password_hash

from extensions import db, login_manager
from forms import RegisterForm ,LoginForm


def create_app():

    app = Flask(__name__)

    app.config["SECRET_KEY"] = "hotelprojectsecret"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"


    db.init_app(app)
    login_manager.init_app(app)

    from models import User
    from flask_login import login_user, logout_user, login_required
    from werkzeug.security import check_password_hash



    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.route("/", methods=["GET", "POST"])
    def login():

        form = LoginForm()

        if form.validate_on_submit():

            user = User.query.filter_by(email=form.email.data).first()

            if user and check_password_hash(user.password, form.password.data):

                login_user(user)

                return redirect(url_for("home"))

            else:
                flash("Invalid Email or Password", "danger")

        return render_template("login.html", form=form)

    @app.route("/register", methods=["GET", "POST"])
    def register():

        form = RegisterForm()

        if form.validate_on_submit():

            hashed_password = generate_password_hash(form.password.data)

            new_user = User(
                name=form.name.data,
                email=form.email.data,
                password=hashed_password
            )

            db.session.add(new_user)
            db.session.commit()

            flash("Registration Successful!", "success")

            return redirect(url_for("register"))

        return render_template("register.html", form=form)



    @app.route("/logout")
    @login_required
    def logout():

        logout_user()

        return redirect(url_for("login"))
    
    @app.route("/home")
    @login_required
    def home():
        return render_template("home.html")

    from models import Room, Booking
    from flask_login import current_user


    @app.route("/rooms")
    @login_required
    def rooms():

        all_rooms = Room.query.all()

        return render_template("rooms.html", rooms=all_rooms)

    @app.route("/book/<int:room_id>", methods=["GET", "POST"])
    @login_required
    def book(room_id):

        room = Room.query.get_or_404(room_id)

        if request.method == "POST":

            date = request.form["date"]

            new_booking = Booking(
                user_id=current_user.id,
                room_id=room.id,
                date=date
            )

            db.session.add(new_booking)
            db.session.commit()

            flash("Room Booked Successfully!", "success")

            return redirect(url_for("mybookings"))

        return render_template("book.html", room=room)


    @app.route("/mybookings")
    @login_required
    def mybookings():

        bookings = Booking.query.filter_by(
            user_id=current_user.id
        ).all()

        return render_template(
            "mybookings.html",
            bookings=bookings
        )


    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
