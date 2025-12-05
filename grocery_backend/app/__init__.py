from flask import Flask
from flask_cors import CORS
from flask_smorest import Api
from .routes.health import blp as health_blp
from .routes.auth import blp as auth_blp
from .routes.products import blp as products_blp
from .routes.cart import blp as cart_blp
from .routes.orders import blp as orders_blp
from .models import db, Product
import os

app = Flask(__name__)
app.url_map.strict_slashes = False
# CORS for React dev on port 3000
CORS(app, resources={r"/api/*": {"origins": ["http://localhost:3000", "http://127.0.0.1:3000", "*"]}})

# Config
app.config["API_TITLE"] = "Grocery Hub API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/docs"
app.config["OPENAPI_SWAGGER_UI_PATH"] = ""
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

# Database configuration: use DATABASE_URL env or default to sqlite file
db_url = os.getenv("DATABASE_URL", "sqlite:///grocery.db")
app.config["SQLALCHEMY_DATABASE_URI"] = db_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

api = Api(app)
db.init_app(app)

def seed_products():
    """Seed some initial grocery products if table is empty."""
    if Product.query.count() > 0:
        return
    sample = [
        {"name": "Bananas", "description": "Fresh ripe bananas", "category": "Fruits", "price": 0.59, "image_url": "", "stock": 200},
        {"name": "Apples", "description": "Crisp red apples", "category": "Fruits", "price": 0.89, "image_url": "", "stock": 150},
        {"name": "Whole Milk 1L", "description": "Dairy milk 1 liter", "category": "Dairy", "price": 2.49, "image_url": "", "stock": 80},
        {"name": "Bread Loaf", "description": "Whole wheat bread", "category": "Bakery", "price": 1.99, "image_url": "", "stock": 60},
        {"name": "Eggs (12)", "description": "Free-range eggs", "category": "Dairy", "price": 3.99, "image_url": "", "stock": 100},
        {"name": "Tomatoes", "description": "Juicy tomatoes", "category": "Vegetables", "price": 1.49, "image_url": "", "stock": 120},
    ]
    for p in sample:
        prod = Product(**p)
        db.session.add(prod)
    db.session.commit()

with app.app_context():
    db.create_all()
    seed_products()

# Register blueprints
api.register_blueprint(health_blp)
api.register_blueprint(auth_blp)
api.register_blueprint(products_blp)
api.register_blueprint(cart_blp)
api.register_blueprint(orders_blp)
