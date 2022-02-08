import logging

from flask_sqlalchemy import Model, SQLAlchemy
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy import inspect

DEFAULT_LOGO_URI = 'https://raw.githubusercontent.com/ant1fact/jalapino/main/static/images/jalapino_150x150.png'


class CRUDModel(Model):
    '''Extended model with integer ID primary key and C(R)UD methods.'''

    # https://flask-sqlalchemy.palletsprojects.com/en/2.x/customizing/#model-class
    @declared_attr
    def id(cls):
        for base in cls.__mro__[1:-1]:
            if getattr(base, '__table__', None) is not None:
                column_type = db.ForeignKey(base.id)
                break
        else:
            column_type = db.Integer

        return db.Column(column_type, primary_key=True)

    def raise_and_rollback(self, e):
        logging.error(e)
        db.session.rollback()
        raise e

    def save(self) -> int:
        '''Saves changes to an existing record or adds a new record to the database
        if it didn't exist and returns its ID on successful creation, otherwise None.'''
        with app.app_context():
            try:
                # Add new object if it didn't exist before
                if self.id is None:
                    db.session.add(self)
                db.session.commit()
                return self.id
            except Exception as e:
                self.raise_and_rollback(e)
            finally:
                db.session.close()

    def update(self, data: dict):
        '''Updates record fields based on a dictionary.'''
        for k, v in data.items():
            if k in self.__class__.__dict__.keys():
                setattr(self, k, v)

    def delete(self) -> int:
        '''Deletes record from database and returns ID if successful, otherwise None.'''
        with app.app_context():
            try:
                self.__class__.query.filter_by(id=self.id).delete()
                db.session.commit()
            except Exception as e:
                self.raise_and_rollback(e)
            finally:
                db.session.close()

    @classmethod
    def required_fields(cls):
        '''Returns column names for the Model class where nullable=False'''
        mapper = inspect(cls)
        not_required = {'id'}
        return [
            c.name
            for c in mapper.columns
            if not c.nullable and c.name not in not_required
        ]


db = SQLAlchemy(model_class=CRUDModel)


class Restaurant(db.Model):
    __tablename__ = 'restaurants'

    # One restaurant per account (unique=True)
    auth0_id = db.Column(db.String(50), unique=True, nullable=False)

    name = db.Column(db.String(50), unique=True, nullable=False)
    logo_uri = db.Column(db.String(250), default=DEFAULT_LOGO_URI)
    description = db.Column(db.String(250))
    address = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    website = db.Column(db.String(250))
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    categories = db.relationship('Category', backref='restaurant')
    orders = db.relationship('Order', backref='restaurant')

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'logo_uri': self.logo_uri,
            'description': self.description,
            'address': self.address,
            'email': self.email,
            'phone': self.phone,
            'website': self.website,
            'categories': [c.serialize() for c in self.categories],
            'orders': [o.serialize() for o in self.orders],
        }


class Customer(db.Model):
    __tablename__ = 'customers'

    # One customer per account (unique=True)
    auth0_id = db.Column(db.String(50), unique=True, nullable=False)

    address = db.Column(db.String(250), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    
    orders = db.relationship('Order', backref='customer')

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'phone': self.phone,
            'orders': [o.serialize() for o in self.orders],
        }


class Category(db.Model):
    '''Item category for visual sorting of items in a resturant's item list.'''

    __tablename__ = 'categories'

    items = db.relationship('Item', backref='group')
    name = db.Column(db.String(50), nullable=False)
    restaurant_id = db.Column(
        db.Integer, db.ForeignKey('restaurants.id'), nullable=False
    )

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'items': [item.serialize() for item in self.items],
        }


items_ingredients = db.Table(
    'items_ingredients',
    db.Column('item_id', db.Integer, db.ForeignKey('items.id'), primary_key=True),
    db.Column(
        'ingredient_id', db.Integer, db.ForeignKey('ingredients.id'), primary_key=True
    ),
)

orders_items = db.Table(
    'orders_items',
    db.Column('orders_id', db.Integer, db.ForeignKey('orders.id'), primary_key=True),
    db.Column('item_id', db.Integer, db.ForeignKey('items.id'), primary_key=True),
)


class Item(db.Model):
    '''Items that can be ordered from a restaurant, such as food and drinks.'''

    __tablename__ = 'items'

    description = db.Column(db.String(250))
    name = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Numeric(5, 2), nullable=False)

    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    ingredients = db.relationship(
        'Ingredient',
        secondary=items_ingredients,
        lazy=False,
        backref=db.backref('items'),
    )

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'ingredients': [i.serialize() for i in self.ingredients],
        }


class Ingredient(db.Model):
    __tablename__ = 'ingredients'

    name = db.Column(db.String(20), unique=True, nullable=False)

    def serialize(self):
        return {'id': self.id, 'name': self.name}


class Order(db.Model):
    __tablename__ = 'orders'

    items = db.relationship(
        'Item', secondary=orders_items, lazy=False, backref=db.backref('orders')
    )
    restaurant_id = db.Column(
        db.Integer, db.ForeignKey('restaurants.id'), nullable=False
    )
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    is_completed = db.Column(db.Boolean, nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'customer_id': self.customer_id,
            'restaurant_id': self.restaurant_id,
            'items': [item.serialize() for item in self.items],
            'is_completed': self.is_completed,
        }


# Importing create_app after assigning db avoids circular import issue
from . import create_app

app = create_app()
