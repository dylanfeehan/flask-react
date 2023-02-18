from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import datetime
from flask_marshmallow import Marshmallow
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

CORS(app)

db = SQLAlchemy(app)

ma = Marshmallow(app)

class Books(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(100))
  body = db.Column(db.Text(5000))
  date = db.Column(db.DateTime, default=datetime.datetime.now())

  def __init__(self, title, body):
    self.title = title
    self.body = body

# lets see if we can do it without this
#def init_db():
  #with app.app_context():
    #db.create_all()

class BooksSchema(ma.Schema):
  class Meta:
    fields = ('id', 'title', 'body', 'date')

book_schema = BooksSchema()
books_schema = BooksSchema(many=True)

@app.route("/")
def index():
  return "this is the homepage. go to /putdata/ to put the data"

@app.route("/getdata/")
def get_books():
  all_books = Books.query.all()
  results = books_schema.jsonify(all_books)
  return results

# get arcticle by id
@app.route("/get/<id>/", methods=['GET'])
def post_details(id):
  article = Books.query.get(id)
  return book_schema.dump(article)

@app.route('/update/<id>/', methods=['GET'])
def update_book(id):
  book = Books.query.get(id)

  #title = request.json['title']
  #body = request.json['body']
  title = 'CHANGED_INTERNALLY'
  body = "body was also changed internally.."

  book.title = title
  book.body = body

  db.session.commit()

  return book_schema.jsonify(book)

@app.route("/delete/<id>", methods=["GET"])
def book_delete(id):
  book = Books.query.get(id)
  db.session.delete(book)
  db.session.commit()
  return book_schema.jsonify(book)

@app.route("/putdata/")
def put_book():
  title = "How To Be Free"
  body = "this is a book written by a stoic philosopher on how to live freely"

  book = Books(title, body)
  db.session.add(book)
  db.session.commit()
  return "i have placed the data in the database. go to /getdata/ to see it"

  # we'll see if we can do it without the create all here..
  if __name__ == "__main__":
    #db.create_all()
    app.run(debug=True)