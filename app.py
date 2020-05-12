from flask import Flask, redirect, url_for, render_template, request, flash, session
from models import *
from forms import ContactForm
from flask_session import Session
from sqlalchemy import and_
import requests


#key
key = "UVD8w0gOPRawwpiWg6WDA"
# Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'my secret'
app.config['DEBUG'] = True

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///book.sqlite'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/book'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
# Session(app)

@app.route("/")
def index():
    '''
    Home page
    '''
    session['user'] = None
    return render_template("home.html")

@app.route("/sign_up")
def sign_up():
    return render_template("sign_up.html", text = "Sign me up!", url = "sign_up_result",error_text="")

@app.route("/sign_in")
def sign_in():
    return render_template("sign_up.html",text = "Sign me in!", url = "sign_in_result",error_text="")


@app.route("/sign_up_result", methods = ["POST"])
def sign_up_result():
    username = request.form.get("username")
    password = request.form.get("password")
    print(username)

    to_add = User(name=username,password=password)
    check = User.query.get(username)
    if check:
        return render_template("sign_up.html",text = "Sign me up!", url = "sign_in_result",error_text="username already taken")
    else:
        db.session.add(to_add)
        db.session.commit()
        return redirect(url_for("search_page"))

    

@app.route("/sign_in_result", methods = ["POST"])
def sign_in_result():
    username = request.form.get("username")
    password = request.form.get("password")
    check = User.query.get(username)
    if not check:
        return render_template("sign_up.html",text = "Sign me in!", url = "sign_in_result",error_text="no such username")
    else:
        if password == check.password:
            session["user"]=username
            return redirect(url_for("search_page"))
        else:
            return render_template("sign_up.html",text = "Sign me in!", url = "sign_in_result",error_text="wrong password")

@app.route("/search_page", methods = ["GET","POST"])
def search_page():
    if request.method == "GET":
        return render_template("search_page.html", list = [])
    else:
        title = request.form.get("title")
        ISBN = request.form.get("ISBN")
        author = request.form.get("author")
        bruh = Book.query.filter( and_(Book.name.startswith(title) , Book.author.startswith(author) , Book.ISBN.startswith(ISBN))).all()
        # and Book.ISBN.startswith(ISBN) and Book.author.startswith(author)
        return render_template("search_page.html", list = bruh)

@app.route("/book/<b>",methods = ["GET","POST"])
def book(b):
    book = Book.query.get(b)
    user = session['user']
    if request.method=="POST":
        comment = request.form.get('comment')
        rating = (request.form.get('rating'))
        book.add_review(rating=rating,comment=comment,name=user)

    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": key, "isbns": b})
    print(res.json())
    data = res.json()
    print(data['books'])
    average_now = float(data['books'][0]['average_rating'])
    # average_now = 5
    number = int(data['books'][0]['work_ratings_count'])
    Reviews = book.reviews
    sum =0
    num = 0
    for Review in Reviews:
        print(Review.comment)
        sum += int(Review.rating)
        num+=1
    average_now = average_now*number
    average_now+=sum
    num+=number
    average = average_now/num

    return render_template("book.html", book=book,average=average, reviews = Reviews,user=user)


if __name__ == "__main__":
    app.run()
    #host="0.0.0.0"
