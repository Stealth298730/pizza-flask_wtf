from flask import Blueprint, render_template, request, redirect

from models.base import Session
from models.pizza import Pizza
from models.ingredient import Ingredient
from data.wheather import get_wheather
from flask import render_template
from flask import Flask, url_for, redirect


pizza_route = Blueprint("pizzas", __name__)


@pizza_route.get("/")
def index():
    wheather = get_wheather("Neratovice")
    temp = wheather.get("temp")
    pizza_name = "Невідома піцца"
    if temp is not None:
        if 26 > temp > 10:
            pizza_name = "Тепла"
        elif temp <= 10:
            pizza_name = "Холодна"
        elif temp > 26:
            pizza_name = "Пепероні"


    return render_template("index.html", title="Моя супер піцерія", wheather=wheather, pizza_name=pizza_name)


@pizza_route.get("/menu/")
def menu():
    wheather = get_wheather("Kyiv")
    with Session() as session:
        pizzas = session.query(Pizza).all()
        ingredients = session.query(Ingredient).all()

        context = {
            "pizzas": pizzas,
            "ingredients": ingredients,
            "title": "Мега меню",
            "wheather": wheather
        }
        return render_template("menu.html", **context)


@pizza_route.post("/add_pizza/")
def add_pizza():
    with Session() as session:
        name = request.form.get("name")
        price = request.form.get("price")
        ingredients = request.form.getlist("ingredients")
        ingredients = session.query(Ingredient).where(Ingredient.id.in_(ingredients)).all()

        pizza = Pizza(name=name, price=price, ingredients=ingredients)
        session.add(pizza)
        session.commit()
        return redirect("/menu/")
    


@pizza_route.get("/pizza/del/<int:id>/")
def del_pizza(id):
    with Session() as session:
        pizza = session.query(Pizza).where(Pizza.id == id).first()
        session.delete(pizza)
        session.commit()
        return redirect(url_for("pizzas.menu"))


@pizza_route.get("/pizza/edit/<int:id>/")
@pizza_route.post("/pizza/edit/<int:id>/")
def edit_pizza(id):
    with Session() as session:
        pizza = session.query(Pizza).where(Pizza.id == id).first()
        if request.method == "POST":
            name = request.form.get("name")
            price = request.form.get("price")

            pizza.name = name
            pizza.price = price
            session.commit()
            
            return redirect(url_for("pizzas.menu"))

        return render_template("edit_pizza.html", pizza=pizza)
    
@pizza_route.get("/poll/")
def poll():
    with Session() as session:
        pizzas = session.query(Pizza).all()
        question = "Яка піца сподобалась найбільше?"
    return render_template("poll.html",question=question,pizzas=pizzas)



@pizza_route.get("/add_vote/")
def add_vote():
    pizza= request.args.get("pizza")
    with open ("data/answers.txt","a",encoding = "utf-8")as file:
        file.write(pizza + "\n")
    return redirect (url_for("pizzas.results"))


@pizza_route.get("/results/")
def results():
    with open("data/answers.txt","r",encoding = "utf-8") as file:
        answers = file.readlines()
        return render_template("results.html",answers=answers)
