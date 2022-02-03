import logging

from flask_sqlalchemy import Model, SQLAlchemy
from sqlalchemy.ext.declarative import declared_attr

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

    def create(self) -> int:
        '''Inserts record into database and returns ID if successful, otherwise None.'''
        with app.app_context():
            try:
                db.session.add(self)
                db.session.commit()
                return self.id
            except Exception as e:
                logging.error(e)
                db.session.rollback()
            finally:
                db.session.close()

    def update(self, data: dict):
        '''Updates record based on a dictionary.'''
        with app.app_context():
            try:
                for k, v in data.items():
                    if k in self.__class__.__dict__.keys():
                        setattr(self, k, v)
                db.session.commit()
            except Exception as e:
                logging.error(e)
                db.session.rollback()
            finally:
                db.session.close()

    def delete(self) -> int:
        '''Deletes record from database and returns ID if successful, otherwise None.'''
        with app.app_context():
            # Making sure the record exists before attempting to delete it
            if self.__class__.query.get(self.id).first() is not None:
                try:
                    self.__class__.query.filter_by(id=id).delete()
                    db.session.commit()
                    return id
                except Exception as e:
                    logging.error(e)
                    db.session.rollback()
                finally:
                    db.session.close()


db = SQLAlchemy(model_class=CRUDModel)


class Restaurant(db.Model):
    __tablename__ = 'restaurants'

    # Should be unique=True for production but it makes development impractical
    auth0_id = db.Column(db.String(50), unique=False, nullable=False)

    name = db.Column(db.String(50), unique=True, nullable=False)
    logo_uri = db.Column(db.String(250), default=DEFAULT_LOGO_URI)
    description = db.Column(db.String(250))
    address = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    website = db.Column(db.String(250))

    categories = db.relationship('Category', backref='restaurant', lazy='subquery')
    orders = db.relationship('Order', backref='restaurant', lazy=True)


class Customer(db.Model):
    __tablename__ = 'customers'

    auth0_id = db.Column(db.String(50), unique=True, nullable=False)

    address = db.Column(db.String(250), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(50), nullable=False)

    orders = db.relationship('Order', backref='customer', lazy=True)


class Category(db.Model):
    '''Item category for visual sorting of items in a resturant's item list.'''

    __tablename__ = 'categories'

    items = db.relationship('Item', backref='group', lazy='subquery')
    name = db.Column(db.String(50), nullable=False)
    restaurant_id = db.Column(
        db.Integer, db.ForeignKey('restaurants.id'), nullable=False
    )


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
        lazy='subquery',
        backref=db.backref('items', lazy=True),
    )


class Ingredient(db.Model):
    __tablename__ = 'ingredients'

    name = db.Column(db.String(20), unique=True, nullable=False)


class Order(db.Model):
    __tablename__ = 'orders'

    items = db.relationship(
        'Item',
        secondary=orders_items,
        lazy='subquery',
        backref=db.backref('orders', lazy=True),
    )
    restaurant_id = db.Column(
        db.Integer, db.ForeignKey('restaurants.id'), nullable=False
    )
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    is_completed = db.Column(db.Boolean, nullable=False)


# Importing create_app after assigning db avoids circular import issue
from . import create_app

app = create_app()
