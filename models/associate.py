from sqlalchemy import Column, String, ForeignKey, Table

from models.base import Base


pizza_ingred_assoc_table = Table(
    "pizza_ingred_assoc_table",
    Base.metadata,
    Column("pizza_id", ForeignKey("pizzas.id"), primary_key=True),
    Column("ingredient_id", ForeignKey("ingredients.id"), primary_key=True)
)