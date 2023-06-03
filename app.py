"""Flask app for Cupcakes"""

from flask import Flask, request, render_template, jsonify

from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, Cupcake

app = Flask(__name__)
app.app_context().push()

app.config['SECRET_KEY'] = "abcdef"

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///cupcakes"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

connect_db(app)

with app.app_context():
    db.create_all()

# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

@app.route('/')
def root():
    """Display homepage"""
    return render_template('homepage.html')


@app.route('/api/cupcakes', methods=['GET'])
def list_cupcakes():
    """Return all cupcakes in system (in JSON format)"""
    cupcakes = [cupcake.to_dict() for cupcake
                in Cupcake.query.all()]
    return jsonify(cupcakes=cupcakes)


@app.route('/api/cupcakes/<int:cc_id>', methods=['GET'])
def get_cupcake(cc_id):
    """Return a cupcake in system (in JSON format) based on id"""
    cupcake = Cupcake.query.get_or_404(cc_id)
    cupcake = cupcake.to_dict()
    return jsonify(cupcake=cupcake)


@app.route('/api/cupcakes', methods=['POST'])
def create_cupcake():
    """Create a cupcake with flavor, size, rating and image data from the body of the request. Respond with JSON info for that cupcake"""
    data = request.json

    new_cupcake = Cupcake(
        flavor=data['flavor'],
        rating=data['rating'],
        size=data['size'],
        image=data['image'] or None
    )

    db.session.add(new_cupcake)
    db.session.commit()

    return (jsonify(cupcake=new_cupcake.to_dict()), 201)


@app.route('/api/cupcakes/<int:cc_id>', methods=['PATCH'])
def update_cupcake(cc_id):
    """Update a cupcake in system based on id"""
    cupcake = Cupcake.query.get_or_404(cc_id)
    
    cupcake.flavor = request.json.get('flavor', cupcake.flavor)
    cupcake.size = request.json.get('size', cupcake.size)
    cupcake.image = request.json.get('image', cupcake.image)
    cupcake.rating = request.json.get('rating', cupcake.rating)

    db.session.commit()

    return jsonify(cupcake=cupcake.to_dict())


@app.route('/api/cupcakes/<int:cc_id>', methods=['DELETE'])
def delete_cupcake(cc_id):
    """Delete a cupcake in system based on id"""
    cupcake = Cupcake.query.get_or_404(cc_id)
    
    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message='Deleted')

