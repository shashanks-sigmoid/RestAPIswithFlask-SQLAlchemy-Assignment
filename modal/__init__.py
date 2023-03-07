from database import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.dialects.postgresql import ARRAY


class Product(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  status = db.Column(db.String(100))
  copy_right = db.Column(db.String(200))
  num_results = db.Column(db.Integer)
  last_modified = db.Column(db.DateTime, default=datetime.utcnow)
  results = db.Column(JSON)

  def __init__(self, status, copy_right, num_results, last_modified, results):
    self.status = status
    self.copy_right = copy_right
    self.num_results = num_results
    self.last_modified = last_modified
    self.results = results
  
class Review(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  status = db.Column(db.String(100))
  copy_right = db.Column(db.String(200))
  num_results = db.Column(db.Integer)
  results = db.Column(JSON)

  def __init__(self, status, copy_right, num_results, results):
    self.status = status
    self.copy_right = copy_right
    self.num_results = num_results
    self.results = results