from flask_smorest import Blueprint, abort
from flask.views import MethodView
from sqlalchemy import or_
from app.models import Product
from app.schemas import ProductSchema, ProductQuerySchema

blp = Blueprint("Products", "products", url_prefix="/api/products", description="Product catalog endpoints")


@blp.route("")
class ProductsList(MethodView):
    @blp.arguments(ProductQuerySchema, location="query")
    @blp.response(200, ProductSchema(many=True))
    def get(self, args):
        """List products with optional search or category filter and pagination."""
        search = args.get("search")
        category = args.get("category")
        page = int(args.get("page", 1))
        page_size = min(int(args.get("page_size", 20)), 100)

        q = Product.query
        if search:
            like = f"%{search}%"
            q = q.filter(or_(Product.name.ilike(like), Product.description.ilike(like)))
        if category:
            q = q.filter(Product.category == category)

        items = q.order_by(Product.name.asc()).paginate(page=page, per_page=page_size, error_out=False).items
        return items


@blp.route("/<int:product_id>")
class ProductDetail(MethodView):
    @blp.response(200, ProductSchema)
    def get(self, product_id: int):
        """Get product detail by ID."""
        product = Product.query.get(product_id)
        if not product:
            abort(404, message="Product not found")
        return product
