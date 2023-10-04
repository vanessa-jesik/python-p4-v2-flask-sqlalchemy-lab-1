# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate
from models import Earthquake, db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route("/")
def index():
    body = {"message": "Flask SQLAlchemy Lab 1"}
    return make_response(body, 200)


# Add views here
@app.route("/earthquakes/<int:id>")
def earthquake_by_id(id):
    earthquake = Earthquake.query.filter_by(id=id).first()
    if earthquake:
        body = {
            "id": earthquake.id,
            "magnitude": earthquake.magnitude,
            "location": earthquake.location,
            "year": earthquake.year,
        }
        status = 200
    else:
        body = {"message": f"Earthquake {id} not found."}
        status = 404
    return make_response(body, status)


@app.route("/earthquakes/magnitude/<float:magnitude>")
def earthquake_by_magnitude(magnitude):
    earthquakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    body = {
        "count": len(earthquakes),
        "quakes": [
            {
                "id": earthquake.id,
                "location": earthquake.location,
                "magnitude": earthquake.magnitude,
                "year": earthquake.year,
            }
            for earthquake in earthquakes
        ],
    }
    status = 200
    return make_response(body, status)


if __name__ == "__main__":
    app.run(port=5555, debug=True)
