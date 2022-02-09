# cd backend
# python -m data.populate_db

import json
from pathlib import Path

from api import create_app
from api.models import Category, Ingredient, Item, Restaurant

app = create_app()
with app.app_context():

    def get_unique_ingredients(restaurants_data: list) -> set:
        ingredients = []
        for restaurant in restaurants_data:
            for items in restaurant['categories'].values():
                for item in items:
                    try:
                        ingredients += item['ingredients']
                    except KeyError:
                        continue
        return set(ingredients)

    def get_id_by_name(ModelClass, name: str) -> int:
        return ModelClass.query.filter_by(name=name).first().id

    def prepare_categories(categories_data: dict, r_id: int) -> list:
        categories = [Category(name=c, restaurant_id=r_id) for c in categories_data]
        for c in categories:
            category_id = c.save()
            for item in categories_data[c.name]:
                i = Item()
                updates = {**item, 'category_id': category_id}
                try:
                    updates['ingredients'] = [
                        Ingredient.query.get(get_id_by_name(Ingredient, name))
                        for name in item['ingredients']
                    ]
                except KeyError:
                    continue
                i.update(updates)
                i.save()
                c.items.append(i)
                c.save()
        return categories

    restaurants_json_path: Path = Path(__file__).parent / 'restaurants.json'
    with open(restaurants_json_path) as f:
        restaurants_data: list = json.load(f)

    ingredients = get_unique_ingredients(restaurants_data)
    ingredients_transient = [Ingredient(name=i) for i in ingredients]
    for i in ingredients_transient:
        i.save()

    for restaurant in restaurants_data:
        r = Restaurant()
        r.update({**restaurant, 'categories': []})
        r_id = r.save()
        categories = prepare_categories(restaurant['categories'], r_id)
        r.update({'categories': categories})
        r.save()
