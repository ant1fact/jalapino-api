from flask_sqlalchemy import Model, SQLAlchemy
from sqlalchemy import inspect

DEFAULT_LOGO_URI = 'https://raw.githubusercontent.com/ant1fact/jalapino/main/static/images/jalapino_150x150.png'
PROTECTED_COLUMN_NAMES = {'id', 'auth0_id'}


class CRUDModel(Model):
    '''Extended model with C(R)UD methods.'''

    def save(self) -> int:
        '''Save changes to an existing record or add a new record to the database
        if it didn't exist and return its ID on successful creation, otherwise None.'''
        try:
            if inspect(self).transient:
                db.session.add(self)
            db.session.commit()
            return self.id
        except Exception as error:
            db.session.rollback()
            return error
        finally:
            db.session.close()

    def update(self, data: dict):
        '''Update row data based on a dictionary.'''
        for k, v in data.items():
            mapper = inspect(self.__class__)
            column_names = [
                c.name for c in mapper.columns if c.name not in PROTECTED_COLUMN_NAMES
            ]
            if k in column_names:
                # It is important to use setattr() instead of directly setting the value
                # on the self, otherwise the changes cannot be tracked by SQLAlchemy
                setattr(self, k, v)

    def delete(self) -> int:
        '''Delete record from database and return ID if successful, otherwise None.'''
        try:
            self.__class__.query.filter_by(id=self.id).delete()
        except Exception as error:
            db.session.rollback()
            return error
        finally:
            db.session.close()

    @classmethod
    def defaults(cls):
        '''Return a dict of of <column name>:<default value> pairs for the given Model.
        If no default value is specified, the value will be None instead.'''

        mapper = inspect(cls)

        def _get_column_default_value(column):
            try:
                return column.default.arg
            except AttributeError:
                return None

        return {
            col.name: _get_column_default_value(col)
            for col in mapper.columns
            if col.name not in PROTECTED_COLUMN_NAMES
        }


db = SQLAlchemy(model_class=CRUDModel)


class Restaurant(db.Model):
    __tablename__ = 'restaurants'

    # One restaurant per account (unique=True)
    # ! unique=False for development only
    auth0_id = db.Column(db.String(50), unique=False, nullable=False)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    logo_uri = db.Column(db.String(250), default=DEFAULT_LOGO_URI)
    description = db.Column(db.String(250), default='')
    address = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    website = db.Column(db.String(250), default='')
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    categories = db.relationship(
        'Category', backref='restaurant', cascade='all, delete-orphan', lazy=False
    )
    orders = db.relationship('Order', backref='restaurant')

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'phone': self.phone,
            'address': self.address,
            'email': self.email,
            'logo_uri': self.logo_uri,
            'description': self.description,
            'website': self.website,
            'categories': [c.serialize() for c in self.categories],
            'orders': [o.serialize() for o in self.orders],
        }


class Customer(db.Model):
    __tablename__ = 'customers'

    # One customer per account (unique=True)
    auth0_id = db.Column(db.String(50), unique=True, nullable=False)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(250), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    orders = db.relationship('Order', backref='customer')

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'orders': [o.serialize() for o in self.orders],
        }


class Category(db.Model):
    '''Item category for visual sorting of items in a resturant's item list.'''

    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    items = db.relationship(
        'Item', backref='category', cascade='all, delete-orphan', lazy=False
    )
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

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(250), default='')
    price = db.Column(db.Numeric(5, 2), nullable=False)

    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    ingredients = db.relationship(
        'Ingredient',
        secondary=items_ingredients,
        lazy='subquery',
        backref=db.backref('items', lazy=True),
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

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)

    def serialize(self):
        return {'id': self.id, 'name': self.name}


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    restaurant_id = db.Column(
        db.Integer, db.ForeignKey('restaurants.id'), nullable=False
    )

    items = db.relationship(
        'Item',
        secondary=orders_items,
        lazy='subquery',
        backref=db.backref('orders', lazy=True),
    )

    def serialize(self):
        return {
            'id': self.id,
            'customer_id': self.customer_id,
            'restaurant_id': self.restaurant_id,
            'items': [item.serialize() for item in self.items],
        }
