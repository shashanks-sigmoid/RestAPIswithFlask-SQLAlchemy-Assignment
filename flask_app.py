from flask import Flask, request, jsonify
from database import db,mm
from modal import Product
from datetime import datetime
import os

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init db
db.init_app(app)
# Init ma
mm.init_app(app)



# Product Schema
class ProductSchema(mm.Schema):
  class Meta:
    fields = ('id', 'status', 'copy_right', 'num_results', 'last_modified','results')

# Init schema
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

# Create a Product
@app.route('/product', methods=['POST'])
def add_product():
  status = request.json['status']
  copy_right = request.json['copy_right']
  num_results = request.json['num_results']
  last_modified = datetime.strptime(request.json['last_modified'], '%Y-%m-%dT%H:%M:%S%z')
  results = request.json['results']
  
  db.create_all()

  new_product = Product(status, copy_right, num_results, last_modified, results)
 
  db.session.add(new_product)
  db.session.commit()

  return product_schema.jsonify(new_product)

# Get All Products
@app.route('/products', methods=['GET'])
def get_products():
  all_products = Product.query.all()
  result = products_schema.dump(all_products)
  print(result[0]['results']['books'])
  return jsonify(result)



# Run Server
if __name__ == '__main__':
  app.run(port=5050,debug=True)