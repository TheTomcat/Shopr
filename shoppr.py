from app import create_app, db
from app.models import Recipe, BaseItem, Ingredient, Shop, Aisle, Mealplan, ShoppingList, ShoppingListItem, User, populate

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 
            'Recipe':Recipe, 
            "BaseItem":BaseItem, 
            "Ingredient":Ingredient, 
            "Shop":Shop, 
            "Aisle":Aisle, 
            "Mealplan":Mealplan, 
            "ShoppingList":ShoppingList, 
            "ShoppingListItem":ShoppingListItem, 
            "User":User,
            "populate": populate,
            "db":db
            }