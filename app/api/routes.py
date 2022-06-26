from flask import abort, jsonify, request
from app.models import *
from app.api import bp


def url_to_query(BaseObject):
    query = BaseObject.query
    if term := request.args.get('q'):
        query = query.filter(BaseObject.name.ilike(f'%{term}%'))
    return query

@bp.get('/recipes')
def get_recipes():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    query = Recipe.process_url(request)
    data = Recipe.to_collection_dict(query, page, per_page, 'api.get_recipes')
    return jsonify(data)

@bp.get('/recipe/<int:recipe_id>')
def get_recipe(recipe_id: int):
    return Recipe.query.get_or_404(recipe_id).to_dict()

@bp.post('/recipe')
def new_recipe():
    body = request.get_json()
    if name := body.get('name'):
        r = Recipe(name=body)
    else:
        abort(400)