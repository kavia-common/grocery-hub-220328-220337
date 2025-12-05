from flask import request
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from app.models import db, CartItem, Order, OrderItem, Product, User
from app.schemas import OrderCreateSchema, OrderSchema
from .auth import _parse_token

blp = Blueprint("Orders", "orders", url_prefix="/api/orders", description="Order endpoints")


def _get_user_from_header() -> User:
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        abort(401, message="Missing token")
    token = auth.split(" ", 1)[1]
    return _parse_token(token)


@blp.route("")
class OrdersCollection(MethodView):
    @blp.response(200, OrderSchema(many=True))
    def get(self):
        """List orders for current user."""
        user = _get_user_from_header()
        orders = Order.query.filter_by(user_id=user.id).order_by(Order.created_at.desc()).all()
        return orders

    @blp.arguments(OrderCreateSchema)
    @blp.response(201, OrderSchema)
    def post(self, data):
        """Create an order from current user's cart. Address is placeholder."""
        user = _get_user_from_header()
        cart_items = CartItem.query.filter_by(user_id=user.id).all()
        if not cart_items:
            abort(400, message="Cart is empty")
        total = 0.0
        order = Order(user_id=user.id, total_amount=0.0, status="created")
        db.session.add(order)
        db.session.flush()
        for ci in cart_items:
            product = Product.query.get(ci.product_id)
            price = float(product.price)
            total += price * ci.quantity
            oi = OrderItem(order_id=order.id, product_id=product.id, quantity=ci.quantity, price=price)
            db.session.add(oi)
        order.total_amount = total
        # clear cart
        for ci in cart_items:
            db.session.delete(ci)
        db.session.commit()
        return order
