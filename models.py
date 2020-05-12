from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import csv

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///book.sqlite'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/book'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'

    name = db.Column(db.String(80), primary_key=True)
    password = db.Column(db.String(20), nullable=False, unique=False)

class Book(db.Model):
    __tablename__ = 'books'
    ISBN = db.Column(db.String(80), primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    author = db.Column(db.String(80), nullable=False)
    year = db.Column(db.String(80), nullable=False)
    reviews = db.relationship("Review", backref="Book",lazy=True)
    
    def add_review(self,rating,comment,name):
        r = Review(rating = rating, comment=comment, Book_ISBN=self.ISBN,Review_writer=name)
        db.session.add(r)
        db.session.commit()

class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False, unique=False)
    comment = db.Column(db.String(256), nullable=True,unique=False)
    Review_writer = db.Column(db.String(80),nullable=False)
    Book_ISBN = db.Column(db.String(20),db.ForeignKey("books.ISBN"),nullable = False)


def main():
    f = open("books.csv")
    reader = csv.reader(f)
    for isbn, title, author, year in reader:
        flight = Book(ISBN=isbn, name=title, author=author,year=year)
        db.session.add(flight)
        # print(f"Added flight from {origin} to {destination} lasting {duration} minutes.")
    db.session.commit()

if __name__ == "__main__":
    db.create_all()
    main()
