from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from topsis import topsis

db = SQLAlchemy()

app = Flask(__name__)

app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI = "mysql://root:123456@localhost/dss",
        SQLALCHEMY_TRACK_MODIFICATIONS = False
    )

db.init_app(app)

@app.route('/')
def index():
   return render_template('home.html')

@app.route('/assistant', methods=["POST"])
def assist():
    data = request.json
    if(data is None):
        return jsonify({'message': 'Data is null'})

if __name__ == 'main':
    app.run(port=5000, debug=True, threaded=True, host='0.0.0.0')