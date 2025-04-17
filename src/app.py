from flask import Flask
from blueprints.floor import app as FloorBlueprint
from blueprints.linen_type import app as LinenTypeBlueprint
from database import db
from middleware import check_api_key

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.sort_keys = False

app.before_request(check_api_key)

db.init_app(app)

with app.app_context():
    db.create_all()

app.register_blueprint(FloorBlueprint)
app.register_blueprint(LinenTypeBlueprint)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
