from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from topsis import bestPrice, bestArea

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
    # Get arguments from request
    price = request.args.get('price')
    address = request.args.get('address')
    # Get all houses
    houses = House.query.all()
    # filter_houses is a list containing houses which match conditions (price and address)
    filter_houses = []
    if address == "hanoi":
        for house in houses:
            print(house.address)
            if "Hà Nội" in house.address:
                price = float(price)
                if (float(house.price) <= price + price*0.15) and (float(house.price) >= price - price*0.3):
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
    elif address == "hcm":
        for house in houses:
            if "Hồ Chí Minh" in house.address:
                price = float(price)
                if (float(house.price) <= price + price*0.15) and (float(house.price) >= price - price*0.3):
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
    length = len(filter_houses)
    # Define a matrix
    matrix = [[0 for x in range(4)] for x in range(length)] 
    # Bring value to matrix (price, area, bedroom_number, floor_number)
    i = 0
    for house in filter_houses:
        matrix[i][0] = float(house['price'])
        matrix[i][1] = house['area']
        matrix[i][2] = house['bedroom_number']
        matrix[i][3] = house['floor_number']
        i = i + 1
    # Calculate C of each house using topsis
    weight = bestPrice(matrix)
    for i in range(length):
        filter_houses[i]['weight'] = weight[i]
    filter_houses.sort(key=lambda x: x['weight'], reverse=True)
    print(filter_houses)

    return render_template('home.html', houses=filter_houses)

if __name__ == '__main__':
    db.create_all()
    app.jinja_env.auto_reload = True
    app.run(port=5000, debug=True, threaded=True, host='0.0.0.0')