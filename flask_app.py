from flask import Flask, request, jsonify
from database import db, ma
from modal import Product, Review
from datetime import datetime
import os

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# Database
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init db
db.init_app(app)
# Init ma
ma.init_app(app)

# Product Schema
class ProductSchema(ma.Schema):
  class Meta:
    fields = ('id', 'status', 'copy_right', 'num_results', 'last_modified','results')

# Init Product schema
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

# Product Schema
class ReviewSchema(ma.Schema):
  class Meta:
    fields = ('id', 'status', 'copy_right', 'num_results','results')

# Init Product schema
review_schema = ReviewSchema()
reviews_schema = ReviewSchema(many=True)

# Create a List
@app.route('/list', methods=['POST'])
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

# Get All Lists
@app.route('/lists', methods=['GET'])
def get_products():
  all_products = Product.query.all()
  result = products_schema.dump(all_products)
  return jsonify(result)

# Get All Best-Sellers NYT
@app.route('/lists/names.json', methods=['GET'])
def get_bestseller_NYT():
  all_products = Product.query.all()
  result = products_schema.dump(all_products)
  book=[]
  for lists in result:
    for list in lists["results"]["lists"]:
        book.append(list["books"][0])
  return jsonify(book)

# Get All Best-Sellers NYT based on date and name
@app.route('/lists/<date>/<name>', methods=['GET'])
def get_books_with_date_and_name(date,name):
  all_products = Product.query.all()
  result = products_schema.dump(all_products)
  books=[]
  for element in result:
    if element["results"]["bestsellers_date"]==date:
        for list in element["results"]["lists"]:
            if list["list_name_encoded"]==name[:-5]:
                books.append(list)       
  return jsonify(books)

# Get All Best-Sellers NYT based on current(latest) date and name
@app.route('/lists/current/<name>', methods=['GET'])
def get_books_with_current_date_and_name(name):
  all_products = Product.query.all()
  result = products_schema.dump(all_products)
  books=[]
  sorted_result_list_by_bestseller_date=sorted(result, key=lambda x:x["results"]["bestsellers_date"])
  current_date=sorted_result_list_by_bestseller_date[0]["results"]["bestsellers_date"]
  for element in result:
    if element["results"]["bestsellers_date"]==current_date:
        for list in element["results"]["lists"]:
            if list["list_name_encoded"]==name[:-5]:
                books.append(list)       
  return jsonify(books)

# Create a Review
@app.route('/review', methods=['POST'])
def add_review():
  status = request.json['status']
  copy_right = request.json['copy_right']
  num_results = request.json['num_results']
  results = request.json['results']
  
  db.create_all()

  new_review = Review(status, copy_right, num_results, results)
 
  db.session.add(new_review)
  db.session.commit()

  return review_schema.jsonify(new_review)

# Get All Review
@app.route('/reviews', methods=['GET'])
def get_reviews():
  all_reviews = Review.query.all()
  result = reviews_schema.dump(all_reviews)
  return jsonify(result)


# Get reviews based on params
@app.route('/reviews.json', methods=['GET'])
def get_review_query():
    book_author=request.args.get("author")
    book_title=request.args.get("title")
    isbn13=request.args.get("isbn")
    if book_author:
        all_reviews = Review.query.filter(Review.results[0]["book_author"].contains(book_author))
    elif book_title:
        all_reviews = Review.query.filter(Review.results[0]["book_title"].contains(book_title))
    elif isbn13:
        all_reviews = Review.query.filter(Review.results[0]["isbn13"].contains([isbn13]))
        
    result = reviews_schema.dump(all_reviews)
    return jsonify(result)


if __name__ == "__main__":
    app.run(port=5050, debug = True)