from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from topsis import topsis


app = Flask(__name__)

app.config.from_mapping(
    SQLALCHEMY_DATABASE_URI = "mysql://root:123456@localhost/dss",
    SQLALCHEMY_TRACK_MODIFICATIONS = False,
    TEMPLATES_AUTO_RELOAD = True
)

db = SQLAlchemy(app)

class House(db.Model):
    __tablename__ = 'house'
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(500))
    price = db.Column(db.Float)
    area = db.Column(db.Float)
    date_created = db.Column(db.String(50))
    image = db.Column(db.String(500))
    floor_number = db.Column(db.Integer)
    bedroom_number = db.Column(db.Integer)
    on_street = db.Column(db.Integer)
    status = db.Column(db.Integer)

@app.route('/')
def index():
    price = request.args.get('price')
    address = request.args.get('address')
    houses = House.query.all()
    filter_houses = []
    if address == "hanoi":
        for house in houses:
            if "Hà Nội" in house.address:
                if (float(house.price) <= price + price*0.2) and (float(house.price) >= price - price*0.4):
                    filter_houses.append({
                        'id': house.id,
                        'address': house.address,
                        'price': house.price,
                        'area': house.area,
                        'date_created': house.date_created,
                        'image': house.image,
                        'floor_number': house.floor_number,
                        'bedroom_number': house.bedroom_number,
                        'on_street': house.on_street,
                        'status': house.status
                    })
    if address == "hcm":
        for house in houses:
            if "Quận" in house.address or "Hồ Chí Minh" in house.address:
                price = float(price)
                if (float(house.price) <= price + price*0.2) and (float(house.price) >= price - price*0.4):
                    filter_houses.append({
                        'id': house.id,
                        'address': house.address,
                        'price': house.price,
                        'area': house.area,
                        'date_created': house.date_created,
                        'image': house.image,
                        'floor_number': house.floor_number,
                        'bedroom_number': house.bedroom_number,
                        'on_street': house.on_street,
                        'status': house.status
                    })
    return render_template('home.html', houses=filter_houses)

if __name__ == '__main__':
    db.create_all()
    app.jinja_env.auto_reload = True
    app.run(port=5000, debug=True, threaded=True, host='0.0.0.0')