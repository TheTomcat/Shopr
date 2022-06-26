from datetime import datetime
from typing import Union
from sqlalchemy.ext.associationproxy import association_proxy
from flask_sqlalchemy import BaseQuery
from flask import url_for

from app import db

class PaginatedAPIMixin(object):
    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
        resources = query.paginate(page, per_page, False)
        data = {
            'items': [item.to_dict() for item in resources.items],
            '_meta': {
                'page': page,
                'per_page': per_page,
                'total_pages': resources.pages,
                'total_items': resources.total
            },
            '_links': {
                'self': url_for(endpoint, page=page, per_page=per_page,
                                **kwargs),
                'next': url_for(endpoint, page=page + 1, per_page=per_page,
                                **kwargs) if resources.has_next else None,
                'prev': url_for(endpoint, page=page - 1, per_page=per_page,
                                **kwargs) if resources.has_prev else None
            }
        }
        return data

meals_recipes = db.Table('meals_recipes', 
                         db.Column('meal_id', db.Integer, db.ForeignKey('meals.meal_id'), primary_key=True),
                         db.Column('recipe_id', db.Integer, db.ForeignKey('recipes.recipe_id'), primary_key=True))

aisles_items = db.Table('aisles_items',
                        db.Column('aisle_id', db.Integer, db.ForeignKey('aisles.aisle_id'), primary_key=True),
                        db.Column('baseitem_id', db.Integer, db.ForeignKey('baseitems.baseitem_id'), primary_key=True))

class Meal(db.Model, PaginatedAPIMixin):
    __tablename__ = 'meals'
    meal_id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String)

    recipes = db.relationship('Recipe', secondary=meals_recipes, back_populates="meals")
    mealplans = db.relationship("Mealplan", back_populates="meal")

    @classmethod
    def get(self, meal_id: int) -> "Meal":
        return Meal.query.filter(meal_id=meal_id).first()

    def to_dict(self) -> dict:
        return {
            'meal_id':self.meal_id,
            'description': self.description,
            'recipes': [recipe.to_dict_min() for recipe in self.recipes]
        }

class Recipe(db.Model, PaginatedAPIMixin):
    __tablename__ = 'recipes'
    recipe_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    instructions = db.Column(db.String)
    preparation_time = db.Column(db.Integer)
    cooking_time = db.Column(db.Integer)
    serves = db.Column(db.Integer)
    
    _added_on = db.Column(db.DateTime, default=datetime.now())

    ingredients = db.relationship("Ingredient", back_populates="recipe")
    baseitems = association_proxy("ingredients", "baseitem")
    meals = db.relationship('Meal', secondary=meals_recipes, back_populates="recipes")

    @classmethod
    def process_url(cls, request) -> BaseQuery:
        query = cls.query
        if name := request.args.get('name'):
            query = query.filter(cls.name.ilike(f'%{name}%'))
        if datefrom := request.args.get('from'):
            pass
        return query

    def to_dict(self) -> dict:
        return {
            'name':self.name,
            'recipe_id':self.recipe_id,
            'ingredients':[ingredient.to_dict() for ingredient in self.ingredients],
            'instructions':self.instructions,
            'preparation_time':self.preparation_time,
            'cooking_time':self.cooking_time,
            'serves':self.serves,
            '_added_on':self._added_on
        }
    
    def to_dict_min(self):
        return {
            'name': self.name,
            'recipe_id': self.recipe_id
        }
    
    @classmethod
    def create_from_dict(cls, dict) -> "Recipe":
        recipe = cls(name=dict['name'], instructions=dict['instructions'], _added_on=datetime.now())
        for ingredient in dict['ingredients']:
            # TODO: Find or create ingredient
            recipe.add_ingredient(ingredient)
        return recipe

    def add_ingredient(self, baseitem: "BaseItem", quantity: Union[int, float], units: str='', preparation: str=''): 
        ingredient = Ingredient(baseitem=baseitem, quantity=quantity, units=units, preparation=preparation)
        self.ingredients.append(ingredient)
    
    @classmethod
    def get(cls, recipe_id) -> "Recipe":
        return cls.query.filter(recipe_id=recipe_id).first()

class BaseItem(db.Model, PaginatedAPIMixin):
    __tablename__ = 'baseitems'
    baseitem_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    ingredients = db.relationship("Ingredient", back_populates="baseitem")
    aisles = db.relationship("Aisle", secondary=aisles_items, back_populates="baseitems")
    shops = association_proxy('aisles', 'shop')
    shoppinglistitems = db.relationship('ShoppingListItem', back_populates="baseitem")

    @classmethod
    def get(cls, item_id: int) -> "BaseItem":
        return BaseItem.query.filter(baseitem_id=item_id).first()

    @classmethod
    def get_by_name(cls, name:str) -> BaseQuery:
        return BaseItem.query.filter(BaseItem.name.ilike(f'%{name}%'))

    def to_dict(self) -> dict:
        return {
            'name': self.name,
            'baseitem_id': self.baseitem_id
        }

    def __repr__(self):
        return f'<BaseItem {self.baseitem_id} - {self.name}>'

class Ingredient(db.Model, PaginatedAPIMixin):
    __tablename__ = 'ingredients'
    ingredient_id = db.Column(db.Integer, primary_key=True)
    baseitem_id = db.Column(db.Integer, db.ForeignKey('baseitems.baseitem_id'))
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.recipe_id'))

    quantity = db.Column(db.Integer)
    units = db.Column(db.String)
    preparation = db.Column(db.String, nullable=True)

    recipe = db.relationship("Recipe", back_populates="ingredients")
    baseitem = db.relationship("BaseItem", back_populates="ingredients")

    @classmethod
    def get(cls, ingredient_id: int) -> "Ingredient":
        return Ingredient.query.filter(ingredient_id=ingredient_id).first()
    
    def to_dict(self) -> dict:
        return {
            'ingredient_id':self.ingredient_id,
            'name': self.baseitem.name,
            'quantity': self.quantity,
            'units': self.units,
            'preparation': self.preparation,
            #'recipe_id':self.recipe_id,
            'baseitem_id':self.baseitem_id
        }

    def __repr__(self):
        return f"<Ingredient id={self.ingredient_id} from {self.recipe.name} ({self.quantity} {self.units} {self.baseitem.name} - {self.preparation})>"


class Shop(db.Model, PaginatedAPIMixin):
    __tablename__ = 'shops'
    shop_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    aisles = db.relationship("Aisle", back_populates="shop")
    baseitems = association_proxy('aisles', 'baseitems')

    def to_dict(self) -> dict:
        return {
            'name': self.name,
            'shop_id': self.shop_id,
            'aisles': [aisle.to_dict() for aisle in self.aisle]
        }

    @classmethod
    def get(cls, shop_id) -> "Shop":
        return Shop.query.filter(shop_id=shop_id).first()

    def create_aisle(self, aisle_name: str):
        return Aisle(name=aisle_name, shop=self)
    
    def __repr__(self):
        return f'<Shop id={self.shop_id} name="{self.name}">'

class Aisle(db.Model):
    __tablename__ = 'aisles'
    aisle_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    # baseitem_id = db.Column(db.Integer, db.ForeignKey('baseitems.baseitem_id'))
    shop_id = db.Column(db.Integer, db.ForeignKey('shops.shop_id'))

    baseitems = db.relationship('BaseItem', secondary=aisles_items, back_populates="aisles")
    shop = db.relationship('Shop', back_populates="aisles")
    
    @classmethod
    def get(cls, aisle_id: int) -> "Aisle":
        return Aisle.query.filter(aisle_id=aisle_id).first()

    def to_dict(self) -> dict:
        return {
            'name':self.name,
            'aisle_id': self.aisle_id
        }

    def add_item(self, item: "BaseItem"):
        self.baseitems.append(item)

    def __repr__(self):
        return f"<Aisle id={self.aisle_id} name='{self.name}' ({self.shop.name})>"

class Mealplan(db.Model, PaginatedAPIMixin):
    __tablename__ = 'mealplans'
    mealplan_id = db.Column(db.Integer, primary_key=True)

    date = db.Column(db.Date)
    meal_id = db.Column(db.Integer, db.ForeignKey('meals.meal_id'))
    meal = db.relationship("Meal", back_populates="mealplans")

class ShoppingList(db.Model):
    __tablename__ = 'shoppinglists'
    shoppinglist_id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)

    shoppinglistitems = db.relationship('ShoppingListItem', back_populates="shoppinglist")

class ShoppingListItem(db.Model):
    __tablename__ = 'shoppinglistitems'
    shoppinglistitem_id = db.Column(db.Integer, primary_key=True)
    shoppinglist_id = db.Column(db.Integer, db.ForeignKey('shoppinglists.shoppinglist_id'))
    baseitem_id = db.Column(db.Integer, db.ForeignKey('baseitems.baseitem_id'))
    quantity = db.Column(db.Integer, default=1)
    is_purchased = db.Column(db.Boolean, default=False)

    shoppinglist = db.relationship('ShoppingList', back_populates="shoppinglistitems")
    baseitem = db.relationship('BaseItem', back_populates="shoppinglistitems")

class User(db.Model, PaginatedAPIMixin):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)


def populate(session):
    r = Recipe(name='Open kibbeh', instructions="", preparation_time=60, cooking_time=45, serves=6)

    r.add_ingredient(baseitem=BaseItem(name='Bulgar Wheat'), quantity=125,units='g')
    r.add_ingredient(baseitem=BaseItem(name='Olive Oil'), quantity=90, units='mL')
    r.add_ingredient(baseitem=BaseItem(name='Garlic'), quantity=2, units='cloves', preparation='crushed')
    r.add_ingredient(baseitem=BaseItem(name='Onion'), quantity=2, preparation='finely chopped')
    r.add_ingredient(baseitem=BaseItem(name='Green Chilli'), quantity=2, preparation="finely chopped")
    r.add_ingredient(baseitem=BaseItem(name='Minced Lamb'), quantity=350, units='g')
    r.add_ingredient(baseitem=BaseItem(name='Allspice'), quantity=1, units='tsp', preparation="ground")
    r.add_ingredient(baseitem=BaseItem(name='Cinnamon'), quantity=1, units='tsp', preparation="ground")
    r.add_ingredient(baseitem=BaseItem(name='Coriander'), quantity=1, units='tsp', preparation="ground")
    r.add_ingredient(baseitem=BaseItem(name='Pine Nuts'), quantity=60, units='g')
    r.add_ingredient(baseitem=BaseItem(name='Parsley'), quantity=3, units='tbsp', preparation="roughly chopped")
    r.add_ingredient(baseitem=BaseItem(name='Self-raising flour'), quantity=2, units='tbsp')
    r.add_ingredient(baseitem=BaseItem(name='Tahini'), quantity=50, units='g')
    r.add_ingredient(baseitem=BaseItem(name='Lemon'), quantity=2, units='tsp', preparation="juiced")
    r.add_ingredient(baseitem=BaseItem(name='Sumac'), quantity=1, units='tsp', preparation="ground")

    session.add(r)
    session.commit()
    return r