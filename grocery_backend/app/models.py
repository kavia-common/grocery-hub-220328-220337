from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class TimestampMixin:
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class User(db.Model, TimestampMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(120), nullable=True)

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)


class Product(db.Model, TimestampMixin):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), index=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(100), index=True, nullable=True)
    price = db.Column(db.Float, nullable=False, default=0.0)
    image_url = db.Column(db.String(500), nullable=True)
    stock = db.Column(db.Integer, nullable=False, default=100)


class CartItem(db.Model, TimestampMixin):
    __tablename__ = "cart_items"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), index=True, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), index=True, nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)

    user = db.relationship(User, backref=db.backref("cart_items", cascade="all, delete-orphan"))
    product = db.relationship(Product)


class Order(db.Model, TimestampMixin):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), index=True, nullable=False)
    total_amount = db.Column(db.Float, nullable=False, default=0.0)
    status = db.Column(db.String(50), nullable=False, default="created")

    user = db.relationship(User, backref=db.backref("orders", cascade="all, delete-orphan"))


class OrderItem(db.Model, TimestampMixin):
    __tablename__ = "order_items"
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), index=True, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), index=True, nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    price = db.Column(db.Float, nullable=False, default=0.0)

    order = db.relationship(Order, backref=db.backref("items", cascade="all, delete-orphan"))
    product = db.relationship(Product)
