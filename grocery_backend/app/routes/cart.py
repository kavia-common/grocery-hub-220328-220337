from flask import request
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from app.models import db, CartItem, Product, User
from app.schemas import CartItemSchema, CartItemCreateSchema, CartItemUpdateSchema
from .auth import _parse_token

blp = Blueprint("Cart", "cart", url_prefix="/api/cart", description="Shopping cart endpoints")


def _get_user_from_header() -> User:
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        abort(401, message="Missing token")
    token = auth.split(" ", 1)[1]
    return _parse_token(token)


@blp.route("")
class CartCollection(MethodView):
    @blp.response(200, CartItemSchema(many=True))
    def get(self):
        """Get cart items for the current user."""
        user = _get_user_from_header()
        items = CartItem.query.filter_by(user_id=user.id).all()
        return items

    @blp.arguments(CartItemCreateSchema)
    @blp.response(201, CartItemSchema)
    def post(self, data):
        """Add an item to the cart. If exists, increase quantity."""
        user = _get_user_from_header()
        product_id = data["product_id"]
        qty = int(data["quantity"])
        product = Product.query.get(product_id)
        if not product:
            abort(404, message="Product not found")
        existing = CartItem.query.filter_by(user_id=user.id, product_id=product_id).first()
        if existing:
            existing.quantity += qty
            db.session.commit()
            return existing
        item = CartItem(user_id=user.id, product_id=product_id, quantity=qty)
        db.session.add(item)
        db.session.commit()
        return item

    @blp.arguments(CartItemUpdateSchema)
    @blp.response(200, CartItemSchema(many=True))
    def put(self, data):
        """Update quantity for a cart item. If quantity=0, remove the item. Return updated cart."""
        user = _get_user_from_header()
        item = CartItem.query.filter_by(id=data["id"], user_id=user.id).first()
        if not item:
            abort(404, message="Cart item not found")
        qty = int(data["quantity"])
        if qty <= 0:
            db.session.delete(item)
        else:
            item.quantity = qty
        db.session.commit()
        items = CartItem.query.filter_by(user_id=user.id).all()
        return items


@blp.route("/<int:item_id>")
class CartItemDetail(MethodView):
    @blp.response(204)
    def delete(self, item_id: int):
        """Remove a cart item by ID."""
        user = _get_user_from_header()
        item = CartItem.query.filter_by(id=item_id, user_id=user.id).first()
        if not item:
            abort(404, message="Cart item not found")
        db.session.delete(item)
        db.session.commit()
        return ""
