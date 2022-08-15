from flask import Flask, jsonify, request
from flask.views import MethodView
from flask_sqlalchemy import SQLAlchemy

app = Flask('app')

# DB connection
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Model Description
class Advert(db.Model):
    __tablename__ = "Advert"

    id = db.Column(db.Integer, primary_key=True)
    header = db.Column(db.String(64), index=True, unique=True)
    description = db.Column(db.String(128))
    create_date = db.Column(db.String(64))
    owner = db.Column(db.String(128))

    def __repr__(self):
        return f"Advert ({self.id}, {self.header}, {self.description}, {self.create_date}, {self.owner})"

# View for Advert items
class AdvertView(MethodView):
    def get(self, advert_id):
        advert = Advert.query.get(advert_id)
        if advert is None:
            raise NotFound
        return jsonify({
            'advert': advert.id,
            'header': advert.header,
            'owner': advert.owner
        })

    def post(self):
        advert_data = request.json
        advert = Advert(**advert_data)
        db.session.add(advert)
        db.session.commit()
        return jsonify({'id': advert.id})

    def delete(self):
        advert_data = request.json
        advert = Advert(**advert_data)
        Advert.query.filter_by(**advert_data).delete()
        db.session.commit()
        return jsonify({'id': advert.id})

# Exception handling
class NotFound(Exception):
    message = 'Not Found'
    status_code = 404

class ValidationError(Exception):
    message = 'Not Valid'
    status_code = 400

@app.errorhandler(ValidationError)
@app.errorhandler(NotFound)
def error_handler(error):
    response = jsonify({'error': error.message})
    response.status_code = error.status_code
    return response

# Routing
app.add_url_rule('/adverts/<int:advert_id>', view_func=AdvertView.as_view('advert_get'), methods=['GET'])
app.add_url_rule('/adverts/', view_func=AdvertView.as_view('advert_post'), methods=['POST'])
app.add_url_rule('/adverts/', view_func=AdvertView.as_view('advert_delete'), methods=['DELETE'])

app.run(port=5000)