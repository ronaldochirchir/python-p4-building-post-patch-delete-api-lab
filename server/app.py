from flask import Flask, request, jsonify
from flask_migrate import Migrate
from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

# Existing GET routes
@app.route('/')
def home():
    return '<h1>Bakery GET-POST-PATCH-DELETE API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries = Bakery.query.all()
    bakeries_serialized = [bakery.to_dict() for bakery in bakeries]
    return jsonify(bakeries_serialized)

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.get_or_404(id)
    return jsonify(bakery.to_dict())

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods_by_price = BakedGood.query.order_by(BakedGood.price.desc()).all()
    baked_goods_by_price_serialized = [bg.to_dict() for bg in baked_goods_by_price]
    return jsonify(baked_goods_by_price_serialized)

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).limit(1).first()
    most_expensive_serialized = most_expensive.to_dict()
    return jsonify(most_expensive_serialized)

# POST /baked_goods
@app.route('/baked_goods', methods=['POST'])
def create_baked_good():
    new_baked_good = BakedGood(
        name=request.form.get('name'),
        price=request.form.get('price'),
        bakery_id=request.form.get('bakery_id')
    )
    
    db.session.add(new_baked_good)
    db.session.commit()
    
    return jsonify(new_baked_good.to_dict()), 201

# PATCH /bakeries/<int:id>
@app.route('/bakeries/<int:id>', methods=['PATCH'])
def update_bakery(id):
    bakery = Bakery.query.get_or_404(id)
    
    if 'name' in request.form:
        bakery.name = request.form.get('name')
    
    db.session.commit()
    
    return jsonify(bakery.to_dict())

# DELETE /baked_goods/<int:id>
@app.route('/baked_goods/<int:id>', methods=['DELETE'])
def delete_baked_good(id):
    baked_good = BakedGood.query.get_or_404(id)
    
    db.session.delete(baked_good)
    db.session.commit()
    
    return jsonify({'message': 'Record successfully deleted'}), 200

if __name__ == '__main__':
    app.run(port=5555, debug=True)