"""Flask app for Cupcakes"""
from models import Cupcake, connect_db, db
from flask import Flask, request, jsonify

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

@app.get('/api/cupcakes')
def show_cupcakes():
    # use example in docstrings
    """this returns dict of cupcakes of JSON
    {cupcakes: [{id, flavor, size, rating, image}, ...]}
    """

    cupcakes = Cupcake.query.all()
    serialized = [c.serialize() for c in cupcakes]

    return jsonify(cupcakes=serialized)

@app.get('/api/cupcakes/<int:cupcake_id>')
def show_single_cupcake(cupcake_id):
    """this returns JSON about single cupcake like
    {cupcake: {id, flavor, size, rating, image}}
    """

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    serialized = cupcake.serialize()

    return jsonify(cupcake=serialized)

@app.post('/api/cupcakes')
def create_cupcake():
    """this create a new cupcake, add to db,
    and returns JSON describing new cupcake
    {cupcake: {id, flavor, size, rating, image}}
    """

    flavor = request.json['flavor']
    size = request.json['size']
    rating = request.json['rating']
    image = request.json['image'] or None

    cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)
    db.session.add(cupcake)
    db.session.commit()

    serialized = cupcake.serialize()

    return (jsonify(cupcake=serialized), 201)

@app.patch('/api/cupcakes/<int:cupcake_id>')
def update_cupcake(cupcake_id):
    """"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    cupcake_copy = request.json.copy()
    print(cupcake_copy)
    breakpoint()
    
    cupcake['flavor'] = cupcake_copy['flavor'] or cupcake['flavor']
    cupcake['size'] = cupcake_copy['size'] or cupcake['size']
    cupcake['rating'] = cupcake_copy['rating'] or cupcake['rating']
    cupcake['image'] = request.json['image'] or cupcake['image']

    db.session.commit()
