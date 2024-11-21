from flask import Flask

from routes.pizza import pizza_route
from models.pizza import Pizza
from models.ingredient import Ingredient
from models.base import create_db
from flask import Flask, render_template, request, redirect

from db.base import Session, create_db
from db.models import Review, Grade
from forms.forms import ReviewForm

app = Flask(__name__)
app.register_blueprint(pizza_route)


app.secret_key = "123"
@app.route("/review/", methods=["GET", "POST"])
def add_review():
    with Session() as session:
        form = ReviewForm()
        grades = session.query(Grade).all()
        if request.method == "POST":
            grade_id = form.grade.data
            text = form.text.data
            author = form.author.data

            review = Review(text=text, author=author, grade_id=grade_id)
            session.add(review)
            session.commit()
            return redirect("/reviews/")
        
        form.grade.choices = []
        for grade in grades:
            form.grade.choices.append((grade.id, grade.value))

        return render_template("add_review")
    return render_template("add_review.html",form = form)
@app.get("/reviews/")
def show_reviews():
    with Session() as session:
        reviews = session.query(Review).all()
        return render_template("reviews.html", reviews=reviews)
if __name__ == "__main__":
    create_db()
    app.run(debug=True,port=5001)